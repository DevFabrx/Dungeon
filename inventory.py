from StateHandler import StateHandler
from State import State
import util
from gamedata import GameData
from player import Player



class Inventory(StateHandler):
    StateHandler.__init__(self, Inventory.start, [], Quit, gamedata)
