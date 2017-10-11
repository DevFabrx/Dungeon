#!/usr/bin/env python3

import json
from player import Player
from item import Item


def check_input(player_input, **allowed_input):
    if player_input in allowed_input:
        return True
    else:
        return False


def print_character(character):
  print("Name: {0}".format(character.name))
  print("Class: {0}".format(character.type))
  print("Attributes:")
  print("\tStrength: {0}".format(character.strength))
  print("\tAgility: {0}".format(character.agility))
  print("\tSpeed: {0}".format(character.speed))
  print("\tDefense: {0}".format(character.defense))
  print("\tSpecial Skill: {0}".format(character.special))

def print_character_stats(character):
  print("Name: {0}".format(character.name))
  print("Attributes:")
  print("\tStrength: {0}".format(character.strength))
  print("\tAgility: {0}".format(character.agility))
  print("\tSpeed: {0}".format(character.speed))
  print("\tDefense: {0}".format(character.defense))

def open_treasure(items):
    print("You found:")
    for i in items:
        print("{0} /t price: {2}".format(items[i].name, items[i].price))
        print("{0} /t value: {2}".format(items[i].influenced_attribute, items[i].value))


def load_player(savefile):
  fp = open(savefile, "r")
  player = Player(**json.load(fp))
  fp.close()
  items = []
  for dict_item in player.inventory:
    item = Item(**dict_item)
    items.append(item)
  player.inventory = items
  return player

def reset_player_stats(gamedata):
    for stat in vars(gamedata.player):
        if type(stat) == int:
          vars(gamedata.player)[stat] = 0
        elif type(stat) == str:
          vars(gamedata.player)[stat] = ""
        else:
          vars(gamedata.player)[stat] = []
    return gamedata



def create_player_file(gamedata):
  with open("player.json", "w") as outfile:
    json.dump(gamedata.player, outfile, cls=CustomEncoder)
    # jstring = json.dumps({"speed": 25, "agility": 25, "special": 0, "defense": 25, "name": "Hans", "inventory": [{"price": 5, "value": 10, "influenced_attribute": "hp", "name": "Potion"}, {"price": 5, "value": 10, "influenced_attribute": "hp", "name": "Potion"}, {"price": 10, "value": 4, "influenced_attribute": "strength", "name": "Beer"}, {"price": 15, "value": 40, "influenced_attribute": "hp", "name": "Bottle of Rum"}], "lvl": 1, "hp": 100, "xp": 0, "type": "", "gold": 109, "strength": 25})
  return outfile

class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Player):
      return obj.__dict__
    if isinstance(obj, Item):
      return obj.__dict__
    else:
      return json.JSONEncoder.default(self,obj)





