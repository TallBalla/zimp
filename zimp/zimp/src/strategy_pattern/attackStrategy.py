from abc import abstractmethod, ABC


class AttackStrategy(ABC):
    def __init__(self, context):
        self.context = context

    def attack(self, item: any) -> None:
        pass
