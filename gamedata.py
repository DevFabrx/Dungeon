#!/usr/bin/env python3
from item import Item

health_potion = Item(name="Health Potion", influenced_attribute="hp", value=25, price=5)
strength_potion = Item(name="Strength Potion", influenced_attribute="strength", value=10, price=30)
speed_potion = Item(name="Speed Potion", influenced_attribute="speed", value=10, price=40)
agility_potion = Item(name="Agility Potion", influenced_attribute="agility", value=10, price=30)
druid_offerings = [health_potion, strength_potion, speed_potion, agility_potion]

corslet = Item(name="Corslet", price=5, influenced_attribute="defense", value=2)
sword = Item(name="Sword", price=10, influenced_attribute="strength", value=4)
helmet = Item(name="Helmet", price=15, influenced_attribute="defense", value=6)
smith_offerings = [corslet, sword, helmet]


class GameData:
    def __init__(self, **gamedata):
        self.player = None
        self.chest = []
        self.druid_offerings = druid_offerings
        self.smith_offerings = smith_offerings
