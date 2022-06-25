from .attackStrategy import AttackStrategy


class AttackContext:
    def __init__(self, attack_strategy: AttackStrategy) -> None:
        self.__attack_strategy = attack_strategy

    def attack(self, *item_names: list[str]) -> None:
        self.__attack_strategy.attack(*item_names)
