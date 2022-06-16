from .attackStrategy import AttackStrategy


class AttackContext:
    def __init__(self, attack_strategy: AttackStrategy):
        self.__attack_strategy = attack_strategy

    def set_attack_strategy(self, attack_strategy: AttackStrategy) -> None:
        self.__attack_strategy = attack_strategy

    def attack(self, *item: any) -> None:
        self.__attack_strategy.attack(*item)
