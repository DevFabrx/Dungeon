from StateHandler import StateHandler
from item import Item
from State import State
from gamedata import GameData
import util
import math

START, DECIDE, STORE, TAKE, QUIT = range(5)

class Start(State):
    def run(self, gamedata, *args):
        print("Welcome to your chest. Here you can safely store some items.")
        if len(gamedata.chest) == 0:
            print("Currently you do not have anything stored in your chest.")
            return STORE, gamedata
        else:
            print("Here are your currently stored items:")
            util.print_chest_items(gamedata.chest)
            return DECIDE, gamedata

    def next(self, next_state):
        if next_state == STORE:
            return Chest.store
        if next_state == DECIDE:
            return Chest.decide


class Decide(State):
    def run(self, gamedata, *args):
        i = input("Do you want to 'store' or 'take' an item with you? Else 'quit'.\n> ")
        if util.check_input(i, "store", "take", "quit"):
            if i == "store":
                return STORE, gamedata
            if i == "take":
                return TAKE, gamedata
            if i == "quit":
                return QUIT, gamedata
        else:
            print("Please input 'store', 'take' or 'quit'")
            return DECIDE, gamedata

    def next(self, next_state):
        if next_state == STORE:
            return Chest.store
        if next_state == TAKE:
            return Chest.take
        if next_state == QUIT:
            return Chest.quit
        if next_state == DECIDE:
            return Chest.decide


class Store(State):
    def run(self, gamedata, *args):
        if len(gamedata.player.inventory) == 0:
            print("You do not have anything to store.")
            return QUIT, gamedata
        print("This are your items in your inventory:")
        util.print_inventory_contents(gamedata.player)
        i = input("What item do you want to store in your chest? Else 'quit'\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.player.inventory)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            chosen_item = next((x for x in gamedata.player.inventory if x.name == i), None)
            gamedata.chest = []
            gamedata.chest.append(chosen_item)
            print("You have choosen {0} to add to your chest.\nRemoved item from inventory.\n"
                  .format(chosen_item.name))
            gamedata.player.inventory.remove(chosen_item)
            return DECIDE, gamedata
        else:
            print("Please insert the name of the item you want to store or 'quit'.")
            return STORE, gamedata

    def next(self, next_state):
        if next_state == START:
            return Chest.start
        if next_state == DECIDE:
            return Chest.decide
        if next_state == STORE:
            return Chest.store
        if next_state == QUIT:
            return Chest.quit


class Take(State):
    def run(self, gamedata, *args):
        if len(gamedata.chest) == 0:
            print("Your chest is empty.")
            return START, gamedata
        util.print_chest_items(gamedata.chest)
        i = input("What item do you want to take from the chest?\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.chest)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            chosen_item = next((x for x in gamedata.chest if x.name == i), None)
            gamedata.player.inventory.append(chosen_item)
            print("You have choosen {0} to add to your inventory.\nRemoved item from chest.\n"
                  .format(chosen_item.name))
            gamedata.chest.remove(chosen_item)
            return START, gamedata
        else:
            print("Please insert the name of the item you want to take or 'quit'.")
            return TAKE, gamedata

    def next(self, next_state):
        if next_state == START:
            return Chest.start
        if next_state == DECIDE:
            return Chest.decide
        if next_state == TAKE:
            return Chest.take
        if next_state == QUIT:
            return Chest.quit


class Quit(State):
    def run(self, gamedata, *args):
        print("Leaving chest.\n")
        return None, gamedata

    def next(self, next_state):
        pass



class Chest(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Chest.start, [Chest.start, Chest.decide, Chest.take, Chest.store], Chest.quit, gamedata)


Chest.start = Start()
Chest.decide = Decide()
Chest.take = Take()
Chest.store = Store()
Chest.quit = Quit()