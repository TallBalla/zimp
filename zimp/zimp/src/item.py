from interfaces.IItem import IItem


class Item(IItem):
    def __init__(self, name, charges):
        self.name = name
        self.charges = charges

    def get_name(self) -> str:
        return self.name

    def get_charges(self) -> int:
        return self.charges
