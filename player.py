#!/usr/bin/env python3

class Player:
    def __init__(self, **player):
        self.name = ""
        self.type = ""
        self.strength = 0
        self.agility = 0
        self.speed = 0
        self.defense = 0
        self.special = 0
        self.lvl = 1
        self.xp = 0
        self.gold = 100  # testing purpose (salesman)
        self.hp = 100
        self.chest = []
        self.inventory = []
        self.__dict__.update(player)

    def get_ability_point_sum(self):
        total_points = int(self.strength) + int(self.agility) + int(self.speed) + int(self.defense)
        return total_points
