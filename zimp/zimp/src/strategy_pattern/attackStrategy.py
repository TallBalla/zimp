from abc import abstractmethod, ABC


class AttackStrategy(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def attack(self, item_names: list[str]) -> None:
        raise NotImplementedError
