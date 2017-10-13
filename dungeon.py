from StateHandler import StateHandler
from State import State
from gamedata import GameData
import util
from room import Room
from enemy import Enemy
from item import Item
from player import Player
import inventory
START, LOOK, MOVE, OPEN, ATTACK,FIGHT, INVENTORY, MENU, SUCCESS, EXIT, QUIT = range(11)

class Start(State):
    def run(self, gamedata, *args):
        return LOOK, gamedata

    def next(self, next_state):
        return Dungeon.look


class Look(State):
    def run(self, gamedata, *args):
        print(gamedata.rooms[gamedata.room_index].description)
        if len(gamedata.rooms[gamedata.room_index].enemies) == 0:
            gamedata.rooms[gamedata.room_index].print_enemy_stats()
        print("")
        return MENU, gamedata

    def next(self, next_state):
        return Dungeon.menu


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
            if i == str(0):
                return LOOK, gamedata
            elif i == str(1):
                return MOVE, gamedata
            elif i == str(2):
                if gamedata.rooms[gamedata.room_index].treasure is not None:
                    return OPEN, gamedata
                else:
                    print("There is no treasure found in this room.")
                    return MENU, gamedata
            elif i == str(3):
                if len(gamedata.rooms[gamedata.room_index].enemies) != 0:
                    return ATTACK, gamedata
                else:
                    print("There are no enemies in this room.")
                    return MENU, gamedata
            elif i == str(4):
                return INVENTORY, gamedata
            elif i == str(5):
                return EXIT, gamedata
        else:
            print("Please enter a number from 0-5")
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
        elif next_state == ATTACK:
            return Dungeon.attack


class Attack(State):
    def run(self, gamedata, *args):
        if len(gamedata.rooms[gamedata.room_index].enemies) == 0:
            print("No enemies left to attack!")
            return MENU, gamedata
        if len(gamedata.rooms[gamedata.room_index].enemies) != 0:
            gamedata.rooms[gamedata.room_index].print_enemy_stats()
            util.print_player_health(gamedata.player)
            i = input("Which enemy do you want to attack?\n > ")
            # check for the allowed inputs
            allowed_inputs = []
            iterator = 0
            for enemy in gamedata.rooms[gamedata.room_index].enemies:
                allowed_inputs.append(str(iterator))
                iterator += 1
        if util.check_input(i, *allowed_inputs):
            gamedata.target_enemy = int(i)
            return FIGHT, gamedata
        else:
            print("Please choose an enemy to attack.")
            # gamedata.rooms[gamedata.room_index].print_enemy_stats()
            return ATTACK, gamedata

    def next(self, next_state):
        if next_state == FIGHT:
            return Dungeon.fight
        if next_state == ATTACK:
            return Dungeon.attack
        if next_state == MENU:
            return Dungeon.menu


class Fight(State):
    def run(self, gamedata, *args):
        target_enemy = gamedata.rooms[gamedata.room_index].enemies[gamedata.target_enemy] # enemy to be attacked
        player = gamedata.player # player
        player_dmg_to_enemy = util.calc_damage(player, target_enemy)
        target_enemy.hp -= player_dmg_to_enemy
        print("You dealt {0} damage to {1}".format(player_dmg_to_enemy, target_enemy.name))
        if target_enemy.hp <= 0:
            gamedata.player.gold += target_enemy.gold
            print("You killed {0} and earned {1} gold.".format(target_enemy.name, target_enemy.gold))
            gamedata.rooms[gamedata.room_index].enemies.remove(target_enemy)
        for enemy in gamedata.rooms[gamedata.room_index].enemies:
            enemy_dmg_to_player = util.calc_damage(enemy, player)
            player.hp -= enemy_dmg_to_player
            print("{0} dealt {1} damage to {2}".format(enemy.name, enemy_dmg_to_player, player.name))
            if player.hp <= 0:
                gamedata.gravedigger_offerings = player.inventory
                player.inventory =[]
                player.hp = 10
                print("You died!")
                return QUIT, gamedata
        if gamedata.room_index == 4 and len(gamedata.rooms[gamedata.room_index].enemies)==0:
            return SUCCESS, gamedata
        return ATTACK, gamedata

    def next(self, next_state):
        if next_state == ATTACK:
            return Dungeon.attack
        if next_state == QUIT:
            return Dungeon.quit
        if next_state == SUCCESS:
            return Dungeon.success


class Inventory(State):
    def run(self, gamedata, *args):
        inv = inventory.Inventory(gamedata)
        inv_gd = inv.run()
        return MENU, inv_gd

    def next(self, next_state):
        return Dungeon.menu


class Success(State):
    def run(self, gamedata, *args):
        print("You cleared the dungeon and killed the boss!")
        return EXIT, gamedata
    def next(self, next_state):
        return Dungeon.exit



class Open(State):
    def run(self, gamedata, *args):
        util.open_treasure(gamedata.rooms[gamedata.room_index].treasure)
        i = input("Do you want to pick it up? (Y/N)\n> ")
        if util.check_input(i, "Y", "y", "N", "n"):
            if i == "Y" or i == "y":
                gamedata.player.inventory.append(gamedata.rooms[gamedata.room_index].treasure)
                print("Picked up {0}".format(gamedata.rooms[gamedata.room_index].treasure.name))
                return MENU, gamedata
        else:
            print("Please input Y/N")
            return OPEN, gamedata

    def next(self, next_state):
        if next_state == MENU:
            return Dungeon.menu
        if next_state == OPEN:
            return Dungeon.open

class Move(State):
    def run(self, gamedata, *args):
        if gamedata.room_index <= 4:
            if len(gamedata.rooms[gamedata.room_index].enemies) != 0:
                print("You cannot move forward, because there are enemies blocking your way.")
                return MENU, gamedata
            else:
                gamedata.room_index += 1
            return START, gamedata
        else:
            return EXIT, gamedata

    def next(self, next_state):
        if next_state == START:
            return Dungeon.start
        if next_state == EXIT:
            return Dungeon.exit
        if next_state == MENU:
            return Dungeon.menu

class Exit(State):
    def run(self, gamedata, *args):
        print("Leaving Dungeon.\n")
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
       room1.description = "You enter the dungeon through a huge gate, that was build generations ago. The gate is covered in golden \n" \
                           "runes of old speech that should protect anyone from entering the dungeon.\n" \
                           "You enter the dungeon. There is almost no ligth in the cave, so you light up a torch. " \
                           "The light from the torch floods the big hall you find yourself\n" \
                           "standing in. The air in the dungeon is moist and cold and you can sense the presence of something evil."

       room2 = Room()
       room2.description = "In this room you find a treasure"
       room2.treasure = Item(name="Sword", price=100, influenced_attribute="strength", value=40)

       room3 = Room()
       room3_enemy1 = Enemy(name="Uruk-Hai", hp=50, defense=25, strength=2000)
       room3_enemy2 = Enemy(name="Ork Archer", hp=20, agility=25)
       room3.enemies = [room3_enemy1, room3_enemy2]
       room3.description = "There are {0} enemies in this room.".format(len(room3.enemies))

       room4 = Room()
       room4.description = "In this room you find a treasure"
       room4.treasure = Item(name="Sword", price=100, influenced_attribute="strength", value=20)


       room5 = Room()
       room5.enemies = [Enemy(hp=80, defense=30, strength=100, agility=20, name="OLAF", gold=10)]
       room5.description = "In this room you find the Ork King {0}.".format(room5.enemies[0].name)

        # create array of rooms
       rooms = [room1, room2, room3, room4, room5]
       gamedata.rooms = rooms
       gamedata.room_index = 0
       gamedata.target_enemy = None


       StateHandler.__init__(self, Dungeon.start,
                                 [Dungeon.start, Dungeon.look, Dungeon.move, Dungeon.open, Dungeon.attack,
                                  Dungeon.fight, Dungeon.inventory, Dungeon.menu, Dungeon.success,
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
    gamedata.player = Player()
    gamedata.player.strength = 25
    gamedata.player.defense = 20
    gamedata.player.agility = 20
    gamedata.player.speed = 35
    gamedata.player.name = "Horst"
    gamedata.player.inventory = [Item(name="Potion", influenced_attribute="hp", value="30")]
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    dun = Dungeon(gamedata)
    gd = dun.run()
