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
    parser.add_argument("-b", help="Activates b tasks", action='store_true')
    parser.add_argument("--savefile",dest="savefile", help="A player savefile")
    parser.add_argument("--create-player", dest="create_player", action='store_true',
                        help="Create a player save file. Stored to player.json by default")

    parser.set_defaults(create_player=False)
    args = parser.parse_args()


    # create gamedata object that holds game information
    gamedata = GameData()

    if args.savefile is not None:
        if args.b:
            gamedata.b = True
        else:
            gamedata.b = False
        gamedata.player = util.load_player(args.savefile)
        vil = Village(gamedata)
        vil_gd = vil.run()
    elif args.b is True:
        gamedata.b = True
        gamedata.player = Player()
        util.create_player_file(gamedata)
        char = CreateCharacter(gamedata)
        gd = char.run()
        vil = Village(gd)
        gd_vil = vil.run()
    else:
        if args.b is True:
            gamedata.b = True
        else:
            gamedata.b = False
        gamedata.b = False
        gamedata.player = Player()
        util.create_player_file(gamedata)
        char = CreateCharacter(gamedata)
        gd = char.run()
        vil = Village(gd)
        gd_vil = vil.run()


