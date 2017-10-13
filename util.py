#!/usr/bin/env python3

import json
from player import Player
from item import Item
import math


def check_input(player_input, *allowed_inputs):
    if player_input in allowed_inputs:
        return True
    else:
        return False


def calc_damage(attacker, defender):
    attacker_hp = attacker.hp
    attacker_defense = attacker.defense
    attacker_strength = attacker.strength
    attacker_speed = attacker.speed
    attacker_agility = attacker.agility

    attacker_damage_brutto = (attacker_strength * 0.5) + (attacker_speed * 0.2) + (attacker_agility * 0.2)

    defender_hp = defender.hp
    defender_defense = defender.defense
    defender_agility = defender.agility
    defender_speed = defender.speed
    defender_dmg_red = defender_defense*1.2 + defender_agility*0.7 + defender_speed*0.3

    # calculation of damage reduction due to defender stats
    attacker_damage_netto = attacker_damage_brutto * (math.log2(defender_dmg_red)/10)

    return math.ceil(attacker_damage_netto)


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


def open_treasure(treasure):
    print("You found:")
    print("{0} \t price: {1} \t influenced attribute: {2} \t value: {3}".format(
        treasure.name, treasure.price,treasure.influenced_attribute, treasure.value))


def load_player(savefile):
    fp = open(savefile, "r")
    player = Player(**json.load(fp))
    fp.close()
    items = []
    chest = []
    for dict_item in player.inventory:
        item = Item(**dict_item)
        items.append(item)
    player.inventory = items
    for dict_item in player.chest:
        item = Item(**dict_item)
        chest.append(item)
    player.chest = chest
    return player

def print_player_health(player):
    print("You have got {0} hp left!".format(player.hp))

def print_inventory_contents(player):
    for item in player.inventory:
        print("* {0} \t --increases {1} by {2}".format(item.name, item.influenced_attribute, item.value))

def print_retailer_offering(player):
    for item in player.inventory:
        print("* {0} for {1} gold".format(item.name, math.floor(item.price*0.5)))

def print_druid_offering(gamedata):
    for item in gamedata.druid_offerings:
        print("* {0} for {1} gold".format(item.name, item.price))

def print_smith_offering(gamedata):
    for item in gamedata.smith_offerings:
        print("* {0} \t {1} gold \t +{2} {3}".format(item.name, item.price, item.value, item.influenced_attribute))

def print_gravedigger_offering(gamedata):
    for item in gamedata.gravedigger_offerings:
        print("* {0} for {1} gold".format(item.name, math.floor(item.price*0.5)))

def print_chest_items(chest):
    for item in chest:
        print("* {0} \t influenced_attribute={1} \t value={2} \t price={3}".format(item.name, item.influenced_attribute,
                                                                                   item.value, item.price))
def get_inventory_names(inventory):
    name_list =[]
    for item in inventory:
        name_list.append(item.name)
    return name_list

def get_inventory_item(player, item_name):
    return player.inventory[player.inventory.index(item_name)]

def reset_player_stats(gamedata):
    for stat in vars(gamedata.player):
        if type(stat) == int:
            vars(gamedata.player)[stat] = 0
        elif type(stat) == str:
            vars(gamedata.player)[stat] = ""
        else:
            vars(gamedata.player)[stat] = []
    return gamedata

def update_player_stats(player, item):
    if item.influenced_attribute == "hp":
        player.hp += item.value
    elif item.influenced_attribute == "strength":
        player.strength += item.value
    elif item.influenced_attribute == "agility":
        player.agility += item.value
    elif item.influenced_attribute == "speed":
        player.speed += item.value

def update_all_player_stats(player,inventory):
    for item in inventory:
        update_player_stats(player,item)


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
            return json.JSONEncoder.default(self, obj)
