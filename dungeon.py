from StateHandler import StateHandler
from State import State
from gamedata import GameData
import util
from room import Room
from enemy import Enemy
from item import Item

START, LOOK, MOVE, OPEN, FIGHT, ATTACK, INVENTORY, MENU, SUCCESS, EXIT, QUIT = range(11)

# TODO Implement States
class Start(State):
    def run(self, gamedata, *args):
        return LOOK, gamedata
    def next(self, next_state):
        return Dungeon.look


class Look(State):
    def run(self, gamedata, *args):
        print(gamedata.rooms[gamedata.room_index].description)
        return LOOK, gamedata
    def next(self, next_state):
        return Dungeon.look

class Menu(State):
    def run(self, gamedata, *args):
        print("0. \t look around")
        print("1. \t move")
        print("2. \t open")
        print("3. \t attack")
        print("4. \t open inventory")
        print("5. \t run away (leave dungeon)")
        i = input("> ")
        if util.check_input(i, "0","1","2","3","4","5"):
            # TODO return what each number does
            if i == 0:
                print(gamedata.room.description)
                return LOOK, gamedata
            elif i == 1:
                return MOVE, gamedata
            elif i == 2:
                if gamedata.rooms[gamedata.room_index].treasure is not None:
                    return OPEN, gamedata
                else:
                    print("No treasure found in this room")
                    return MENU, gamedata
            elif i == 3:
                if gamedata.rooms[gamedata.room_index].enemies is not None:
                    return FIGHT, gamedata
                else:
                    print("There are no enemies in this room")
                    return MENU, gamedata
            elif i == 4:
                return INVENTORY, gamedata
            elif i == 5:
                return EXIT, gamedata
        else:
            print("Please enter a number from 0-6")
            return MENU, gamedata

    def next(self, next_state):
        if next_state == LOOK:
            return Dungeon.look
        elif next_state == MOVE:
            return Dungeon.move
        elif next_state == OPEN:
            return Dungeon.open
        elif next_state == FIGHT:
            return Dungeon.fight
        elif next_state == INVENTORY:
            return Dungeon.inventory
        elif next_state == MENU:
            return Dungeon.menu
        elif next_state == EXIT:
            return Dungeon.exit


class Fight(State):
    def run(self, gamedata, *args):
        if gamedata.rooms[gamedata.room_index].enemies is not None:


    def next(self, next_state):

class Open(State):
    def run(self, gamedata, *args):
        util.open_treasure()
        i = input("Do you want to take it? (Y/N)")
        if util.check_input(i, "Y", "y", "N", "n"):
            if i == "Y" or i == "y":
                gamedata.player.inventory.append(gamedata.rooms[gamedata.room_index].treasure)
                print("Took {0}".format(gamedata.rooms[gamedata.room_index].treasure.name))
                return
        else:
            print("Please input Y/N")


class Move(State):
    def run(self, gamedata, *args):
        if gamedata.room_index <= 4:
            gamedata.room_index += 1
            return START, gamedata
        else:
            return EXIT, gamedata

    def next(self, next_state):
        if next_state == START:
            return Dungeon.start
        if next_state == EXIT:
            return Dungeon.exit

class Exit(State):
    def run(self, gamedata, *args):
        print("Leaving Dungeon.")
        return Quit, gamedata
    def next(self, next_state):
        return Dungeon.quit

class Quit(State):
    def run(self, gamedata, *args):
        return None, gamedata
    def next(self, next_state):
        pass


class Dungeon(StateHandler):
   def __init__(self,gamedata):

       room1 = Room()
       room1.description = "You enter the dungeon through a huge gate, that was put up generations ago. The gate is covered in golden " \
                             "runes of old speech that should protect anyone from going inside the dungeon." \
                             "There is almost no ligth in the cave, so you light up a torch. The light from the torch floods the big hall you find yourself" \
                             "standing in. The air in the dungeon is moist and cold and you can sense the presence of something evil."

       room2 = Room()
       room2.enemies = [Enemy("Orc", health=30, damage=5), Enemy("Goblin", health=40, damage = 10)]
       room2.description = "You find {0} enemies.".format(len(room2.enemies))

       room3 = Room()
       room3.enemies = [Enemy("Orc", health=30, damage=5), Enemy("Goblin", health=40, damage = 10)]
       room3.description = "You find {0} enemies.".format(len(room3.enemies))

       room4 = Room()
       room4.description = "In this room you find a treasure"
       room4.treasure = Item("Sword", price = 100, influenced_attribute = "damage", value = 40)


       room5 = Room()
       room5.boss = Enemy(health=150, damage=20, type="Boss")
       room5.description = "In this room you find the boss"

        # create array of rooms
       rooms = [room1, room2, room3, room4, room5]
       gamedata.rooms = rooms
       gamedata.room_index = 0


       StateHandler.__init__(self, Dungeon.start,
                                 [Dungeon.start, Dungeon.look, Dungeon.move, Dungeon.open, Dungeon.fight,
                                  Dungeon.attack, Dungeon.inventory, Dungeon.menu, Dungeon.success,
                                  Dungeon.exit, Dungeon.quit], Quit(), gamedata)


# Declaration of Dungeon methods/states
Dungeon.start = Start()
Dungeon.look = Look()
Dungeon.move = Move()
Dungeon.open = Open()
Dungeon.fight = Fight()
Dungeon.attack = Attack()
Dungeon.inventory = Inventory()
Dungeon.menu = Menu()
Dungeon.success = Success()
Dungeon.exit = Exit()
Dungeon.quit = Quit()

if __name__ == '__main__':
    gamedata = GameData()
    player_file = util.create_player_file()
    gamedata.player = util.load_player("player.json")
    dun = Dungeon(gamedata)
    gd = dun.run()
