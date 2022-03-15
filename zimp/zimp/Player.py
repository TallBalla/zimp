from functools import partial
from Item import Item
from View import View

class Player():
    view = View()

    def __init__(self, user_name):
        self._item_one = None
        self._item_two = None
        self.attack = 1
        self.health = 6
        self.user_name = user_name

    # Item one property and setter
    @property
    def item_one(self):
        return self._item_one

    @item_one.setter
    def item_one(self, new_item):
        if self.item_one is not None: 
            self.remove_item_handler(self._item_one)
        self._item_one = new_item
        self.item_prop_handler(new_item)

    # Item two property and setter
    @property
    def item_two(self):
        return self._item_two

    @item_two.setter
    def item_two(self, new_item):
        if self.item_one is not None:
            self.remove_item_handler(self._item_two)
        self._item_two = new_item
        self.item_prop_handler(new_item)

    def check_item_none(self, item):
        return item is None

    def cower(self):
        self.health += 3
        
    def runaway(self):
        self.health -= 1

        if self.check_item_none(self.item_one) or self.check_item_none(self.item_two):
            return

        if self.item_one.get_item_name() is None or self.item_two.get_item_name() is None:
            if self.view.check_use_item("Oil"):
                return 

    def remove_item_handler(self, item):
        self.item_prop_handler(item)
        self.item = None

    # TODO give functionality to this method 
    # This will invole checking if another device exists
    # If it does it increase attack damager
    def combination_handler(self):
        return

    def add_attack(self, item_attack):
        self.attack += item_attack

    def add_health(self, health):
        self.health += health

    def remove_attack(self, attack):
        self.attack -= attack

    def remove_health(self, health):
        self.health -= health

    def get_player_health(self):
        return self.health

    def get_player_attack(self):
        return self.attack

    def check_item_uses(self, item):
        return item.get_use_item() == 0

    # Got partial idea from here 
    # https://stackoverflow.com/questions/36648887/python-switch-case-allowing-optional-arguments
    def item_prop_handler(self, item):
        """ handles all the checks for the tile properties
        to see if they have any special characterics """
        add_props = {
            "add attack 1": partial(self.add_attack, 1),
            "add attack 2": partial(self.add_attack, 2),
            "add health": partial(self.add_health, 1),
            "combination": self.combination_handler,
            }

        add_props.get(item.get_item_prop(), None)()

# TODO remove this only tester code
#player = Player("hello")
#item1 = Item(False, "hammer", "add attack 1", 3)
#item2 = Item(False, "hammer", "add health", 3)

#player.item_one = item1
#print(player.attack)
#print(player.health)
#print(player.item_one.get_item_prop())

#print()

#player.item_one = item2
#print(player.attack)
#print(player.health)
#print(player.item_one.get_item_prop())


