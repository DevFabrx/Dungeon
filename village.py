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
import retailer
import inventory
import dungeon
import chest
import smith
import druid







# define states
START, LIST, CHOOSE, DUNGEON, INVENTORY, RETAILER, SMITH, DRUID, CHEST, SAVE, QUIT = range(11)

class Start(State):
    def run(self, gamedata, *args):
        print("You are now entering the village")
        print("The name of the village is Nurmgrad.")
        print("The weather is cloudy, light rain is falling and people are moving silently in the streets.")
        return LIST, gamedata

    def next(self, next_state):
        return Village.list


class List(State):
    def run(self, gamedata, *args):
        print("Your destinations are:")
        print("0. \t Dungeon")
        print("1. \t Inventory")
        print("2. \t Retailer")
        print("3. \t Smith")
        print("4. \t Druid")
        print("5. \t Chest")
        print("6. \t Save")
        print("7. \t Quit")

        return CHOOSE, gamedata
    def next(self, next_state):
        return Village.choose


class Choose(State):
    def run(self, gamedata, *args):
        i = input("Please choose your destination [0-7]:\n> ")
        print("")
        if util.check_input(i, "0","1","2","3","4","5","6","7"):
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
                return CHEST, gamedata
            elif i == "6":
                return SAVE, gamedata
            elif i == "7":
                return QUIT, gamedata
        else:
            print("Please enter a number from 0-7")
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
        elif next_state == CHEST:
            return Village.chest
        elif next_state == SAVE:
            return Village.save
        elif next_state == QUIT:
            return Village.quit


class Inventory(State):
    def run(self, gamedata, *args):
        inv = inventory.Inventory(gamedata)
        inv_gd = inv.run()
        return LIST, inv_gd
    def next(self, next_state):
        return Village.list


# TODO Implement Smith
class Smith(State):
    def run(self, gamedata, *args):
        sm = smith.Smith(gamedata)
        sm_gd = sm.run()
        return LIST, sm_gd

    def next(self, next_state):
        return Village.list


class Retailer(State):
    def run(self, gamedata, *args):
        ret = retailer.Retailer(gamedata)
        ret_gd = ret.run()
        return LIST, ret_gd
    def next(self, next_state):
        if next_state == LIST:
            return Village.list


#TODO Implement Druid
class Druid(State):
    def run(self, gamedata, *args):
        dr = druid.Druid(gamedata)
        dr_gd = dr.run()
        return LIST, dr_gd

    def next(self, next_state):
        return Village.list


class Dungeon(State):
    def run(self, gamedata, *args):
        dun = dungeon.Dungeon(gamedata)
        dun_gd = dun.run()
        return LIST, dun_gd
    def next(self, next_state):
        if next_state == LIST:
            return Village.list

class Chest(State):
    def run(self, gamedata, *args):
        box = chest.Chest(gamedata)
        box_gd = box.run()
        return LIST, box_gd

    def next(self, next_state):
        if next_state == LIST:
            return Village.list

class Save(State):
    def run(self, gamedata, *args):
        with open("player.json", "w") as outfile:
            json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
        print("Game saved.\n")
        return LIST, gamedata

    def next(self, next_state):
        return Village.list


class Quit(State):
    def run(self, gamedata, *args):
        return None, gamedata
    def next(self, next_state):
        pass


class Village(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Village.start, {Village.start, Village.list, Village.choose, Village.dungeon,
                                                    Village.inventory, Village.retailer,
                                                    Village.smith, Village.druid, Village.chest, Village.save, Village.quit}, Quit(),gamedata)


Village.start = Start()
Village.list = List()
Village.choose = Choose()
Village.dungeon = Dungeon()
Village.inventory = Inventory()
Village.retailer = Retailer()
Village.smith = Smith()
Village.druid = Druid()
Village.chest = Chest()
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
