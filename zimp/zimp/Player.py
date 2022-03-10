class Player():
    def __init__(self, user_name):
        self._item_one = None
        self._item_two = None
        self.attack = 1
        self.healh = 6
        self.user_name = user_name

    # Item one property and setter
    @property
    def item_one(self):
        return self._item_one

    @item_one.setter
    def item_one(self, new_item):
        self._item_one = new_item

    # Item two property and setter
    @property
    def item_two(self):
        return self._item_two

    @item_two.setter
    def item_two(self, new_item):
        self._item_two = new_item

    def check_item_prop(self, item):
        """ handles all the checks for the tile properties
        to see if they have any special characterics """
        # TODO: add methods to these field
        props = {
            "add attack 1": 1,
            "add attack 2": 1,
            "add attack 3": 1,
            "add health": 1,
            "combination": 1,
            }
        props.get(item.item_prop, None)()