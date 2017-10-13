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
            print("Your inventory is empty.")
            return QUIT, gamedata
        print("Welcome to your Inventory {0}".format(gamedata.player.name))
        return LIST, gamedata

    def next(self, next_state):
        if next_state == LIST:
           return Inventory.list
        if next_state == QUIT:
            return Inventory.quit


class List(State):
    def run(self, gamedata, *args):
        if len(gamedata.player.inventory) == 0:
            print("Your inventory is empty.")
            return QUIT, gamedata
        util.print_inventory_contents(gamedata.player)
        i = input("Type 'quit' or the name of the item you want to use/drop:\n> ")
        allowed_inputs = []
        for item in gamedata.player.inventory:
            allowed_inputs.append(item.name)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return QUIT, gamedata
            inventory_names = util.get_inventory_names(gamedata.player.inventory)
            if i in inventory_names:
                chosen_item = next((x for x in gamedata.player.inventory if x.name == i), None)
                i2 = input("Do you want to 'use' or 'drop' {0}? Else 'quit'.\n> "
                           .format(chosen_item.name)) # print name of item
                if util.check_input(i2, "use", "drop", "quit"):  # check if input2 is legal
                    if i2 == "drop":
                        print("Droppend {0}".format(chosen_item.name))
                        gamedata.player.inventory.remove(chosen_item)
                        return LIST, gamedata
                    if i2 == "quit":
                        return LIST, gamedata
                    if i2 == "use":# TODO implement use of potions
                        if chosen_item.type == "consumable":
                            util.update_player_stats(gamedata.player, chosen_item)
                            gamedata.player.inventory.remove(chosen_item)
                            print("Increased your {0} by {1}".format(chosen_item.influenced_attribute, chosen_item.value))
                            return LIST, gamedata
                        else:
                            print("{0} is not consumable. Please choose another item".format(chosen_item.name))
                            return LIST, gamedata

                else:
                    return LIST, gamedata

        else:
            return LIST, gamedata


    def next(self, next_state):
        if next_state == LIST:
            return Inventory.list
        if next_state == QUIT:
            return Inventory.quit


class Choose(State):
    def run(self, gamedata, *args):
        i = input("Type 'quit' or the name of the item you want to sell:\n> ")
        allowed_inputs = util.get_inventory_names(gamedata.player.inventory)
        allowed_inputs.append("quit")
        if util.check_input(i, *allowed_inputs):
            if i == "quit":
                return LIST, gamedata
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
            return Inventory.choose
        if next_state == LIST:
            return Inventory.list

class Quit(State):
    def run(self, gamedata, *args):
        print("Leaving Inventory.\n")
        return None, gamedata
    def next(self, next_state):
        pass




class Inventory(StateHandler):
    def __init__(self,gamedata):
        StateHandler.__init__(self, Inventory.start, [Inventory.start, Inventory.list, Inventory.choose], Inventory.quit, gamedata)


Inventory.start = Start()
Inventory.list = List()
Inventory.choose = Choose()
Inventory.quit = Quit()


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = Player()
    gamedata.player.strength = 25
    gamedata.player.defense = 20
    gamedata.player.agility = 20
    gamedata.player.speed = 35
    gamedata.player.name = "Horst"
    gamedata.player.inventory = [Item(type="consumable",name="Potion", price=50, influenced_attribute="hp", value="30"),
                                 Item(type="consumable",name="Potion", price=50, influenced_attribute="hp", value="30"),
                                 Item(type="consumable",name="Potion", price=50, influenced_attribute="hp", value="30")]
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    ret = Inventory(gamedata)
    ret_gd = ret.run()