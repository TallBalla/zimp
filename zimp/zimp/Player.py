

class Player:
    def __init__(self, attack=1, health=6, x=16, y=16, has_totem=False):
        self.attack = attack
        self.health = health
        self.x = x
        self.y = y
        self.items = []
        self.has_totem = has_totem

    def set_items(self, items: list[str]) -> None:
        self.items = items

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

    def get_items(self) -> list[str]:
        return self.items

    def get_item_charges(self, item_name: str) -> int:
        for check_item in self.get_items():
            if check_item[0] == item_name:
                return check_item[1]

    def set_item_charges(self, item_name: str, charge: int) -> None:
        for check_item in self.get_items():
            if check_item[0] == item_name:
                check_item[1] = charge

    def use_item_charge(self, item_name: str) -> None:
        for check_item in self.get_items():
            if check_item[0] == item_name:
                check_item[1] -= 1

    def add_item(self, item_name: str, charges: int) -> None:
        if len(self.items) < 2:
            self.items.append([item_name, charges])

    def remove_item(self, item: list) -> None:
        self.items.pop(self.items.index(item))

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
