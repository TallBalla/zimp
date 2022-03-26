from Item import Item


class Player():
    def __init__(self, user_name):
        self.items = [Item(None, '', '', None), 
                      Item(None, '', '', None)]
        self.attack = 1
        self.health = 6
        self.user_name = user_name

    def check_item_one_none(self):
        return self.items[0] is None
    
    def check_item_two_none(self):
        return self.items[1] is None

    def check_item_uses(self, item):
        return item.get_use_item() == 0

    def get_attack_items(self):
        attack_items = []
        for item in self.items:
            if 'attack' in item.get_item_prop():
                attack_items.append(item)
        return attack_items

    def get_health_items(self):
        health_items = []
        for item in self.items:
            if 'health' in item.get_item_prop():
                health_items.append(item)
        return health_items

    def get_special_items(self):
        special_items = []
        for item in self.items:
            if 'special' in item.get_item_prop():
                special_items.append(item)
        return special_items


    def get_item(self, name):
        return next(filter(lambda item: item.get_item_name() == name,
                          self.items))

    def cower(self):
        self.health += 3
        
    def runaway(self):
        self.health -= 1

    def add_attack(self, item_attack):
        self.attack += item_attack
    
    def add_health(self, health):
        self.health += health

    def remove_attack(self, attack):
        self.attack -= attack

    def remove_health(self, health):
        self.health -= health

    def decrement_item_one_use(self):
        self.items[0].use_item()

    def decrement_item_two_use(self):
        self.items[1].use_item()

    def get_player_health(self):
        return self.health

    def get_player_attack(self):
        return self.attack

    def get_item_one(self):
        return self.items[0]

    def get_item_two(self):
        return self.items[1]

    def set_item_one(self, item):
        self.items[0] = item

    def set_item_two(self, item):
        self.items[1] = item

    def get_items(self):
        return self.items


    # Got partial idea from here 
    # https://stackoverflow.com/questions/36648887/python-switch-case-allowing-optional-arguments

