import random


class Game():
    """
        Controller, calls all the methods in the correct order
    """
    def __init__(self, start_tile):
        self.available_exits = 0
        self.current_tile = start_tile
        self.devcards = []
        self.tiles = []
        self.time = 9

    def reshuffle(self):
        time += 1
        random.shuffle(devcards)

    def shuffle(self):
        random.shuffle(devcards)
