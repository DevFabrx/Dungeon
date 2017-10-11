import sys
import util
import json
from StateHandler import StateHandler
from player import Player
from gamedata import GameData
from State import State
from dungeon import Dungeon
from inventory import Inventory
from retailer import Retailer
from smith import Smith
from druid import Druid



# define states
START, LIST, CHOOSE, DUNGEON, INVENTORY, RETAILER, SMITH, DRUID, SAVE, QUIT = range(5)

class Start(State):
    def run(self, gamedata, *args):
        print("You are now entering the village")
        print("The name of the village is Nurmgrad")
        print("The weather is cloudy, light rain is falling and people are moving silently in the streets.")

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
        if util.check_input(i, 0,1,2,3,4,5,6):
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
            dungeon_gd = Dungeon(gamedata).run()
            return Village.start
        elif next_state == INVENTORY:
            inventory_gd = Inventory(gamedata).run()
            Village.gamedata = inventory_gd
            return Village.start
        elif next_state == RETAILER:
            retailer_gd = Retailer(gamedata).run()
            Village.gamedata = retailer_gd
            return Village.start
        elif next_state == SMITH:
            smith_gd = Smith(gamedata).run()
            Village.gamedata = smith_gd
            return Village.start
        elif next_state == DRUID:
            druid_gd = Druid(gamedata).run()
            Village.gamedata = druid_gd
            return Village.start
        elif next_state == SAVE:
            return Village.save
        elif next_state == QUIT:
            return Village.quit


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

    def run(self, *args):
        rooms = []
        for i in rooms:
            StateHandler.run()



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
    player_file = util.create_player_file()
    gamedata.player = util.load_player("player.json")
    vil = Village(gamedata)
    gd = vil.run()
