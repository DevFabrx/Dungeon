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
        print("Welcome to the Smith, {0}!".format(gamedata.player.name))
        print("The Smith offers you some armors and weapons to buy that influence your attributes.")
        return LIST, gamedata

    def next(self, next_state):
        if next_state == LIST:
            return Smith.list


class List(State):
    def run(self, gamedata, *args):
        util.print_smith_offering(gamedata)
        print("You have {0} gold.\n".format(gamedata.player.gold))
        return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == QUIT:
            return Smith.quit
        if next_state == CHOOSE:
            return Smith.choose


class Choose(State):
    def run(self, gamedata, *args):
        i = input("Type 'quit' or the name of the item you want to buy:\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.smith_offerings)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            chosen_item = next((x for x in gamedata.smith_offerings if x.name == i), None)
            if gamedata.player.gold < chosen_item.price:
                print("You do not have enough money to buy this item")
                return CHOOSE, gamedata
            gamedata.player.gold -= math.floor(chosen_item.price)
            print("You have choosen {0}.\nYou now have {1} gold.\nAdded item to your inventory.\n"
                  .format(chosen_item.name, gamedata.player.gold))
            gamedata.player.inventory.append(chosen_item)
            return LIST, gamedata
        else:
            print("Please insert the name of the item you want to buy or 'quit'")
            return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return Smith.choose
        if next_state == LIST:
            return Smith.list
        if next_state == QUIT:
            return Smith.quit

class Quit(State):
    def run(self, gamedata, *args):
        print("Leaving Smith.\n")
        return None, gamedata
    def next(self, next_state):
        pass


class Smith(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Smith.start, [Smith.start, Smith.list, Smith.choose], Smith.quit, gamedata)


Smith.start = Start()
Smith.list = List()
Smith.choose = Choose()
Smith.quit = Quit()


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
    ret = Smith(gamedata)
    ret_gd = ret.run()