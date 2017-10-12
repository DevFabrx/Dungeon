from StateHandler import StateHandler
from State import State
from gamedata import GameData
import util
from room import Room
from enemy import Enemy
from item import Item
from player import Player

START, LOOK, MOVE, OPEN, FIGHT, ATTACK, INVENTORY, MENU, SUCCESS, EXIT, QUIT = range(11)

class Start(State):
    def run(self, gamedata, *args):
        return LOOK, gamedata

    def next(self, next_state):
        return Dungeon.look


class Look(State):
    def run(self, gamedata, *args):
        print(gamedata.rooms[gamedata.room_index].description)
        if gamedata.rooms[gamedata.room_index].enemies is not None:
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
                if gamedata.rooms[gamedata.room_index].enemies is not None:
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
        gamedata.rooms[gamedata.room_index].print_enemy_stats()
        i = input("Which enemy do you want to attack? [0-1]")
        # check for the allowed inputs
        if util.check_input(i, "0", "1"):
            gamedata.target_enemy = int(i)
            return FIGHT, gamedata
        else:
            print("Please choose an enemy to attack [0-1]")
            gamedata.rooms[gamedata.room_index].print_enemy_stats()
            return ATTACK, gamedata


    def next(self, next_state):
        if next_state == FIGHT:
            return Dungeon.fight
        if next_state == ATTACK:
            return Dungeon.attack


#TODO Implement Attack State
class Fight(State):
    def run(self, gamedata, *args):
        enemy = gamedata.rooms[gamedata.room_index].enemies[gamedata.target_enemy]
        player = gamedata.player
        damage_to_enemy = util.calc_damage(player, enemy)
        enemy.hp -= damage_to_enemy
        gamedata.rooms[gamedata.room_index].enemies[gamedata.target_enemy].hp = enemy.hp
        print("You dealt {0} damage to {1}.".format(damage_to_enemy, enemy.type))
        if enemy.hp <= 0:
            gamedata.rooms[gamedata.room_index].enemies.remove(enemy)
            print("You killed {0}".format(enemy.type))
        for enemy in gamedata.rooms[gamedata.room_index].enemies:
            damage_to_player = util.calc_damage(enemy, player)
            player.hp -= damage_to_player
            gamedata.player.hp = player.hp
            print("{0} dealt {1} damage to {2}".format(enemy.name, damage_to_player, player.name))
            if player.hp <= 0:
                print("You died.")
                gamedata.player.hp = 10
                gamedata.player.inventory = []
                return QUIT, gamedata


    def next(self, next_state):
        pass


#TODO Implement Inventory State
class Inventory(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass

# TODO implement Success State
class Success(State):
    def run(self, gamedata, *args):
        pass
    def next(self, next_state):
        pass


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
            if gamedata.rooms[gamedata.room_index].enemies is not None:
                print(gamedata.room_index)
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
       room1.description = "You enter the dungeon through a huge gate, that was build generations ago. The gate is covered in golden \n" \
                           "runes of old speech that should protect anyone from going inside the dungeon.\n" \
                           "You enter the dungeon. There is almost no ligth in the cave, so you light up a torch. " \
                           "The light from the torch floods the big hall you find yourself\n" \
                           "standing in. The air in the dungeon is moist and cold and you can sense the presence of something evil."

       room2 = Room()
       room2_enemy1 = Enemy(name="Orc", hp=30)
       room2_enemy2 = Enemy(name="Goblin", hp=15, speed=20)
       room2.enemies = [room2_enemy1, room2_enemy2]
       room2.description = "You find {0} enemies.".format(len(room2.enemies))

       room3 = Room()
       room3_enemy1 = Enemy(name="Uruk-Hai", hp=50, defense=25, strength=20)
       room3_enemy2 = Enemy(name="Ork Archer", hp=20, agility=25)
       room3.enemies = [room3_enemy1, room3_enemy2]
       room3.description = "You find {0} enemies.".format(len(room3.enemies))

       room4 = Room()
       room4.description = "In this room you find a treasure"
       room4.treasure = Item(name="Sword", price=100, influenced_attribute="damage", value=40)


       room5 = Room()
       room5.boss = [Enemy(hp=150, damage=20, type="Boss")]
       room5.description = "In this room you find the boss"

        # create array of rooms
       rooms = [room1, room2, room3, room4, room5]
       gamedata.rooms = rooms
       gamedata.room_index = 0
       gamedata.target_enemy = None


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
    gamedata.player = Player()
    gamedata.player.strength = 25
    gamedata.player.defense = 20
    gamedata.player.agility = 20
    gamedata.player.speed = 35
    gamedata.player.name = "Horst"
    player_file = util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    dun = Dungeon(gamedata)
    gd = dun.run()
