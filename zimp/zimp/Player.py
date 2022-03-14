from functools import partial
from Item import Item

class Player():
    def __init__(self, user_name):
        self._item_one = None
        self._item_two = None
        self.attack = 1
        self.health = 6
        self.user_name = user_name

    def remove_item_handler(self, item):
        self.item_prop_handler(item)
        self.item = None

    # TODO fill out the functionality of w
    def combination_handler(self):
        return "hello"

    def add_attack(self, item_attack):
        self.attack += item_attack

    def add_health(self, health):
        self.health += health

    def remove_attack(self, attack):
        self.attack -= attack

    def remove_health(self, health):
        self.health -= health

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

    # TODO get the method for removing a item sorted
    # Got partial idea from here 
    # https://stackoverflow.com/questions/36648887/python-switch-case-allowing-optional-arguments
    def item_prop_handler(self, item, ):
        """ handles all the checks for the tile properties
        to see if they have any special characterics """
        # TODO: add methods to combination field
        add_props = {
            "add attack 1": partial(self.add_attack, 1),
            "add attack 2": partial(self.add_attack, 2),
            "add attack 3": partial(self.add_attack, 3),
            "add health": partial(self.add_health, 1),
            "combination": self.combination_handler,
            }

        add_props.get(item.get_item_prop(), None)()

# TODO remove this only tester code
player = Player("hello")
item1 = Item(False, "hammer", "add attack 1", 3)
item2 = Item(False, "hammer", "add health", 3)

player.item_one = item1
print(player.attack)
print(player.health)
print(player.item_one.get_item_prop())

print()

player.item_one = item2
print(player.attack)
print(player.health)
print(player.item_one.get_item_prop())


