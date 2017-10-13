#!/usr/bin/env python3

import argparse
import util
import json

from player import Player
from gamedata import GameData
from create_character import CreateCharacter
from village import Village

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="P0 Dungeon")
    parser.add_argument("--savefile",dest="savefile", help="A player savefile")
    parser.add_argument("--create-player", dest="create_player", action='store_true',
                        help="Create a player save file. Stored to player.json by default")
    parser.set_defaults(create_player=False)
    args = parser.parse_args()


    # create gamedata object that holds player information
    gamedata = GameData()


    if args.savefile is not None:
        gamedata.player = util.load_player(args.savefile)
    else:  # args.create_player != None or (args.savefile == None and args.create_player == False):
        gamedata.player = Player()
        util.create_player_file(gamedata)
        gamedata.player = util.load_player("player.json")

    char = CreateCharacter(gamedata)
    gd = char.run()
    vil = Village(gd)
    gd_vil = vil.run()


