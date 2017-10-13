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
        if len(gamedata.player.inventory) == 0:
            print("Sorry you have nothing to sell.")
            print("Thanks for visiting\n")
            return QUIT, gamedata
        print("Welcome to the retailer {0}!".format(gamedata.player.name))
        return LIST, gamedata

    def next(self, next_state):
        if next_state == QUIT:
            return Retailer.quit
        if next_state == LIST:
            return Retailer.list


class List(State):
    def run(self, gamedata, *args):
        if len(gamedata.player.inventory) == 0:
            print("You have nothing to sell left.")
            print("Thanks for visiting.")
            return QUIT, gamedata
        print("This is what I would pay for your items:")
        util.print_retailer_offering(gamedata.player)
        print("You have {0} gold.\n".format(gamedata.player.gold))
        return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == QUIT:
            return Retailer.quit
        if next_state == CHOOSE:
            return Retailer.choose


class Choose(State):
    def run(self, gamedata, *args):
        i = input("Type 'quit' or the name of the item you want to sell:\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.player.inventory)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            chosen_item = next((x for x in gamedata.player.inventory if x.name == i), None)
            gamedata.player.gold += math.floor(chosen_item.price * 0.5)
            print("You have choosen {0}.\nYou now have {1} gold.\nRemoved item from inventory.\n"
                  .format(chosen_item.name, gamedata.player.gold))

            gamedata.player.inventory.remove(chosen_item)
            return LIST, gamedata
        else:
            return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return Retailer.choose
        if next_state == LIST:
            return Retailer.list

class Quit(State):
    def run(self, gamedata, *args):
        print("Leaving Retailer.\n")
        return None, gamedata
    def next(self, next_state):
        pass


class Retailer(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Retailer.start, [Retailer.start, Retailer.list, Retailer.choose], Retailer.quit, gamedata)


Retailer.start = Start()
Retailer.list = List()
Retailer.choose = Choose()
Retailer.quit = Quit()


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
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    ret = Retailer(gamedata)
    ret_gd = ret.run()