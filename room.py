class Room:
    def __init__(self, description=None, enemies=[], treasure=[]):
        self.description = description
        self.enemies = enemies
        self.treasure = treasure

    def print_enemy_stats(self):
        i = 0
        for enemy in self.enemies:
            print("{0}. \t {1} \t health: {2}".format(i, enemy.name, enemy.hp))
            i += 1