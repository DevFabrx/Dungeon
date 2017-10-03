#!/usr/bin/env python3

import argparse
import util
import json

from player import Player
from gamedata import GameData

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="P0 Dungeon")
  parser.add_argument('--savefile', help="A player saveifle")
  parser.add_argument("--create-player", dest="create_player", action='store_true', help="Create a player save file. Stored to player.json by default")
  parser.set_defaults(create_player=False)
  args = parser.parse_args( )
  
  #your code goes here
