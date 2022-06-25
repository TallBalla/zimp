
from interfaces.IDevCard import IDevCard
from item import Item


class DevCard(IDevCard):
    def __init__(self) -> None:
        self.events = []

    def set_flyweight_facotry(self, flyweight_factory) -> None:
        self.flyweight_factory = flyweight_factory

    def get_event_at_time(self, time: int) -> str:
        event_index = time - 9
        if event_index < len(self.events):
            event_index = 0
        return self.events[event_index]

    def add_event(self, type: str, consquence: int) -> None:
        event = self.flyweight_factory.get_event(type, consquence)
        self.events.append(event)

    def set_item(self, name, charges) -> None:
        if charges != "Unlimited":
            int(charges)
        self.item = Item(name, charges)

    def get_item(self) -> str:
        return self.item.get_name()

    def get_charges(self) -> int:
        return self.charges.get_charges()
