class Item():
    def __init__(self, combination, item_name, item_prop, uses):
        self.combination = combination
        self.item_name = item_name
        self.item_prop = item_prop 
        self.uses = uses

    def get_item_prop(self):
        return self.item_prop
