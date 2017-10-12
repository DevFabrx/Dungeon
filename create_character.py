import util
import json
from StateHandler import StateHandler
from player import Player
from gamedata import GameData
from State import State
from village import Village

# define states
START, ASK, STRENGTH, AGILITY, SPEED, DEFENSE, CONFIRM, STORE = range(8)


class Start(State):
    def run(self, gamedata):
        print("Welcome to P0 Dungeon Quest character creator")
        name = input("Give us a name to call you: ")
        gamedata.name = name
        return ASK, gamedata

    def next(self, next_state):
        if next_state == ASK:
            return CreateCharacter.ask


class Ask(State):
    def run(self, gamedata):

        check = input("{0} is the name you want to choose? (Y/N) ".format(gamedata.name))

        if check == "Y" or check == "y":
            gamedata.player.name = gamedata.name
            return STRENGTH, gamedata
        elif check == "N" or check == "n":
            return START, gamedata
        else:
            print("Please enter Y/y for yes or N/n for no!")
            return ASK, gamedata

    def next(self, next_state):
        if next_state == STRENGTH:
            return CreateCharacter.strength
        if next_state == ASK:
            return CreateCharacter.ask
        if next_state == START:
            return CreateCharacter.start


class Strength(State):
    def run(self, gamedata, *args):
        print("You have 100 points to assign to your character.\n Start now to assign those Points to your characters"
              " strength, agility, speed and defense")
        strength = input("assign strength: ")
        gamedata.player.strength = int(strength)
        return AGILITY, gamedata

    def next(self, next_state):
        return CreateCharacter.agility


class Agility(State):
    def run(self, gamedata, *args):
        agility = input("assign agility: ")
        gamedata.player.agility = int(agility)
        return SPEED, gamedata

    def next(self, next_state):
        return CreateCharacter.speed


class Speed(State):
    def run(self, gamedata, *args):
        speed = input("assign speed: ")
        gamedata.player.speed = int(speed)
        return DEFENSE, gamedata

    def next(self, next_state):
        return CreateCharacter.defense


class Defense(State):
    def run(self, gamedata, *args):
        defense = input("assign defense: ")
        gamedata.player.defense = int(defense)
        return CONFIRM, gamedata

    def next(self, next_state):
        return CreateCharacter.confirm


class Confirm(State):
    def run(self, gamedata, *args):
        if int(gamedata.player.getAbilityPointSum()) > 100:
            print("Sorry it seems like you spent more than 100 ability points on your character..."
                  " try that again!")
            util.reset_player_stats(gamedata)
            return STRENGTH, gamedata
        if gamedata.player.getAbilityPointSum() < 100:
            print("You have {0} Points left to use. Do you want to use them?".format(gamedata.player.getAbilityPointSum()))
            i = input("Y/N: ")
            if i == "Y" or i == "y":
                util.reset_player_stats(gamedata)
                return STRENGTH, gamedata
            else:
                pass # continue if player dont want to spend unused points
        util.print_character_stats(gamedata.player)
        check = input("Is this correct? (Y/N) ")
        if check == "Y" or check == "y":
            return STORE, gamedata
        elif check == "N" or check == "n":
            return CONFIRM, gamedata
        else:
            print("Please enter Y/y for yes or N/n for no!")
            return CONFIRM, gamedata

    def next(self, next_state):
        if next_state == STRENGTH:
            return CreateCharacter.strength
        if next_state == STORE:
            return CreateCharacter.store


class Store(State):
    def run(self, gamedata):
        with open("player.json", "w") as outfile:
            json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
        return None, gamedata

    def next(self, next_state):
        pass


class Quit(State):
    def run(self, gamedata):
        return None, gamedata

    def next(self, x):
        pass


class CreateCharacter(StateHandler):
    def __init__(self, gamedata):
        StateHandler.__init__(self, CreateCharacter.start,
                              [CreateCharacter.start, CreateCharacter.ask, CreateCharacter.strength,
                               CreateCharacter.agility, CreateCharacter.speed, CreateCharacter.defense,
                               CreateCharacter.confirm, CreateCharacter.store], Quit(), gamedata)


CreateCharacter.start = Start()
CreateCharacter.ask = Ask()
CreateCharacter.strength = Strength()
CreateCharacter.agility = Agility()
CreateCharacter.speed = Speed()
CreateCharacter.defense = Defense()
CreateCharacter.confirm = Confirm()
CreateCharacter.store = Store()

if __name__ == '__main__':
    gamedata = GameData()
    player = Player()
    gamedata.player = player
    util.create_player_file(gamedata)
    gamedata.player = util.load_player("player.json")
    create_char = CreateCharacter(gamedata)
    create_char_gd = create_char.run()
    village = Village(create_char_gd)
    village_gd = village.run()


