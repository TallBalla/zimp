from abc import ABC


class IItem(ABC):
    def __init__(self, name, charges):
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError

    def get_charges(self) -> int:
        raise NotImplementedError
