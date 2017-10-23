from StateHandler import StateHandler
from State import State
from gamedata import GameData
import util
import math
from player import Player
from item import Item


START, LIST, CHOOSE, QUIT = range(4)

class Start(State):
    def run(self, gamedata, *args):
        if len(gamedata.gravedigger_offerings) == 0:
            print("Gravedigger inventory is empty.")
            return QUIT, gamedata
        print("Welcome to the Gravedigger, {0}!".format(gamedata.player.name))
        print("The Gravedigger offers you your lost inventory if you die in the dungeon.")
        return LIST, gamedata

    def next(self, next_state):
        if next_state == LIST:
            return Gravedigger.list
        if next_state == QUIT:
            return Quit()


class List(State):
    def run(self, gamedata, *args):
        util.print_gravedigger_offering(gamedata)
        print("You have {0} gold.\n".format(gamedata.player.gold))
        return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == QUIT:
            return Quit()
        if next_state == CHOOSE:
            return Gravedigger.choose


class Choose(State):
    def run(self, gamedata, *args):
        if len(gamedata.gravedigger_offerings) == 0:
            print("No items left.")
            return QUIT, gamedata
        i = input("Type 'quit' or the name of the item you want to buy:\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.gravedigger_offerings)
        allowed_inputs.append("quit")
        print(allowed_inputs)
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            chosen_item = next((x for x in gamedata.gravedigger_offerings if x.name == i), None)
            if gamedata.player.gold < chosen_item.price:
                print("You do not have enough money to buy this item")
                return CHOOSE, gamedata
            gamedata.player.gold -= math.floor(chosen_item.price)
            print("You have chosen {0}.\nYou now have {1} gold.\nAdded item to your inventory.\n"
                  .format(chosen_item.name, gamedata.player.gold))
            gamedata.player.inventory.append(chosen_item)
            if chosen_item.type != "consumable":
                util.update_player_stats(gamedata.player, chosen_item)
            gamedata.gravedigger_offerings.remove(chosen_item)
            return LIST, gamedata
        else:
            print("Please insert the name of the item you want to buy or 'quit'")
            util.print_gravedigger_offering(gamedata)
            return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return Gravedigger.choose
        if next_state == LIST:
            return Gravedigger.list
        if next_state == QUIT:
            return Quit()

class Quit(State):
    def run(self, gamedata, *args):
        print("Leaving Gravedigger.\n")
        return None, gamedata
    def next(self, next_state):
        pass


class Gravedigger(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Gravedigger.start, [Gravedigger.start, Gravedigger.list, Gravedigger.choose], Quit(), gamedata)


Gravedigger.start = Start()
Gravedigger.list = List()
Gravedigger.choose = Choose()


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = Player()
    gamedata.player.strength = 25
    gamedata.player.defense = 20
    gamedata.player.agility = 20
    gamedata.player.speed = 35
    gamedata.player.name = "Horst"
    gamedata.player.inventory = [Item(name="Potion", price=50, influenced_attribute="hp", value="30"),
                                 Item(name="Potion", price=50, influenced_attribute="hp", value="30"),
                                 Item(name="Potion", price=50, influenced_attribute="hp", value="30")]
    gamedata.player.gold = 100
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    ret = Gravedigger(gamedata)
    ret_gd = ret.run()