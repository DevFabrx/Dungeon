from player import Player


class Enemy(Player):
    def __init__(self, **player):
        self.name = ""
        self.type = ""
        self.strength = 5
        self.agility = 5
        self.speed = 5
        self.defense = 5
        self.special = 0
        self.lvl = 1
        self.xp = 0
        self.gold = 1  # testing purpose (salesman)
        self.hp = 25
        self.inventory = []
        self.__dict__.update(player)

