from abc import ABC


class IDevCard(ABC):
    def get_item(self) -> str:
        raise NotImplementedError

    def get_charges(self) -> int:
        raise NotImplementedError

    def get_event_at_time(self, time: int) -> str:
        raise NotImplementedError

    def add_event(self, type: str, consquence: int) -> None:
        raise NotImplementedError
