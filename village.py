import sys
import util
import json
from StateHandler import StateHandler
from player import Player
from gamedata import GameData
from State import State
from dungeon import Dungeon
import math
from item import Item





# define states
START, LIST, CHOOSE, DUNGEON, INVENTORY, RETAILER, SMITH, DRUID, SAVE, QUIT = range(10)

class Start(State):
    def run(self, gamedata, *args):
        print("You are now entering the village")
        print("The name of the village is Nurmgrad")
        print("The weather is cloudy, light rain is falling and people are moving silently in the streets.")
        return LIST, gamedata

    def next(self, next_state):
        return Village.list


class List(State):
    def run(self, gamedata, *args):
        print("Your destinations are:")
        print("0 \t Dungeon")
        print("1 \t Inventory")
        print("2 \t Retailer")
        print("3 \t Smith")
        print("4 \t Druid")
        print("5 \t Save")
        print("6 \t Quit")

        return CHOOSE, gamedata
    def next(self, next_state):
        return Village.choose


class Choose(State):
    def run(self, gamedata, *args):
        i = input("Please choose your destination [0-6]: ")
        if util.check_input(i, "0","1","2","3","4","5","6"):
            if i == "0":
                return DUNGEON, gamedata
            elif i ==  "1":
                return INVENTORY, gamedata
            elif i == "2":
                return RETAILER, gamedata
            elif i == "3":
                return SMITH, gamedata
            elif i == "4":
                return DRUID, gamedata
            elif i == "5":
                return SAVE, gamedata
            elif i == "6":
                return QUIT, gamedata
        else:
            print("Please enter a number from 0-6")
            return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return Village.choose
        elif next_state == DUNGEON:
            return Village.dungeon
        elif next_state == INVENTORY:
            return Village.inventory
        elif next_state == RETAILER:
            return Village.retailer
        elif next_state == SMITH:
            return Village.smith
        elif next_state == DRUID:
            return Village.druid
        elif next_state == SAVE:
            return Village.save
        elif next_state == QUIT:
            return Village.quit

class Inventory(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass


# TODO Implement Smith
class Smith(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass

# TODO Implement Retailer
class Retailer(State):
    def run(self, gamedata, *args):
        if len(gamedata.player.inventory) == 0:
            print("Sorry you have nothing to sell.")
            print("Thanks for visiting")
            return LIST, gamedata
        print("Welcome to the retailer {0}!".format(gamedata.player.name))
        print("This is what I would pay for your items:")
        util.print_retailer_offering(gamedata.player)
        print("You have {0} gold.".format(gamedata.player.gold))
        i = input("Type 'quit' or the name of the item you want to sell:\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.player.inventory)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return LIST, gamedata
            chosen_item = next((x for x in gamedata.player.inventory if x.name == i), None)
            gamedata.player.gold += math.floor(chosen_item.price*0.5)
            print("You have chosen {0}.\nYou now have {1} gold.\nRemoved item from inventory."
                  .format(chosen_item.name, gamedata.player.gold))
            gamedata.player.inventory.remove(chosen_item)
        else:
            return RETAILER, gamedata



    def next(self, next_state):
        if next_state == LIST:
            return Village.list
        if next_state == RETAILER:
            return Village.retailer


# TODO Implement Druid
class Druid(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass

class Dungeon(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass

class Save(State):
    def run(self, gamedata, *args):
        with open("player.json", "w") as outfile:
            json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
        return QUIT, gamedata

    def next(self, next_state):
        return Village.quit


class Quit(State):
    def run(self, gamedata, *args):
        return None, gamedata
    def next(self, next_state):
        pass


class Village(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Village.start, {Village.start, Village.list, Village.choose, Village.dungeon,
                                                    Village.inventory, Village.retailer,
                                                    Village.smith, Village.druid, Village.save, Village.quit}, Quit(),gamedata)


Village.start = Start()
Village.list = List()
Village.choose = Choose()
Village.dungeon = Dungeon()
Village.inventory = Inventory()
Village.retailer = Retailer()
Village.smith = Smith()
Village.druid = Druid()
Village.save = Save()
Village.quit = Quit()


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = Player()
    gamedata.player.strength = 25
    gamedata.player.defense = 20
    gamedata.player.agility = 20
    gamedata.player.speed = 35
    gamedata.player.name = "Horst"
    gamedata.player.gold = 100
    gamedata.player.inventory = [Item(name="Potion", price = 15, influenced_attribute="hp", value="30")]
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    vil = Village(gamedata)
    vil_gd = vil.run()
