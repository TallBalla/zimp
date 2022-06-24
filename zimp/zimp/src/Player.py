

from item import Item


class Player:
    def __init__(self, attack=1, health=6, x=16, y=16, has_totem=False):
        self.attack = attack
        self.health = health
        self.x = x
        self.y = y
        self.items = []
        self.has_totem = has_totem

    def get_health(self) -> int:
        return self.health

    def found_totem(self) -> None:
        self.has_totem = True

    def get_attack(self) -> int:
        return self.attack

    def set_attack(self, attack: int) -> None:
        self.attack = attack

    def set_health(self, health: int) -> None:
        self.health = health

    def add_health(self, health: int) -> None:
        self.health += health

    def remove_health(self, health: int) -> None:
        self.health -= health

    def add_attack(self, attack: int) -> None:
        self.attack += attack

    def remove_attack(self, attack: int) -> None:
        self.attack -= attack

    def get_items(self):
        return self.items

    def get_items_names(self):
        return [item.get_name() for item in self.items]

    def get_item_charges(self, item_name: str) -> int:
        for check_item in self.get_items():
            if check_item.get_name() == item_name:
                return check_item.get_charges()

    def set_item_charges(self, item_name: str, charge: int) -> None:
        for check_item in self.get_items():
            if check_item.get_name() == item_name:
                check_item.set_charge(charge)

    def use_item_charge(self, item_name: str) -> None:
        for check_item in self.get_items():
            if check_item.get_name() == item_name:
                check_item.minus_charge(1)

    def add_item(self, item_name: str, charges: int) -> None:
        self.items.append(Item(item_name, charges))

    def remove_item(self, item_name: str) -> None:
        for check_item in self.get_items():
            if check_item.get_name() == item_name:
                self.items.remove(check_item)

    def set_x(self, x: int) -> None:
        self.x = x

    def set_y(self, y: int) -> None:
        self.y = y

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_has_totem(self) -> bool:
        return self.has_totem

    def set_attack(self, attack: int) -> None:
        self.attack = attack

    def set_items(self, items: list[str]) -> None:
        for item in items:
            self.add_item(item[0], item[1])


