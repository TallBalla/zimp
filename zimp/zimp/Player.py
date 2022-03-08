class Player():
    def __init__(self):
        self.attack = 1
        self.health = 6
        self.item_one = None
        self.item_two = None

    def cower(self):
        self.health += 3

    def run_away(self):
        self.health -= 1

    @property
    def item_one(self):
        return self.item_one

    @item_one.setter
    def item_one(self, item):
        self.item_one = item

    @property
    def item_two(self):
        return self.item_two

    @item_two.setter
    def item_two(self, item):
        self.item_two = item
