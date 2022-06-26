from event import Event


class DevCard:
    def __init__(self,
                 item: str,
                 charges: int) -> None:
        self.item = item
        self.charges = charges
        self.events = []

        if self.charges != "Unlimited":
            int(self.charges)

    def get_event_at_time(self, time: int) -> str:
        event_index = time - 9
        if event_index < len(self.events):
            event_index = 0
        return self.events[event_index]

    def add_event(self, type: str, consquence: int) -> None:
        event = Event(type, consquence)
        self.events.append(event)

    def get_item(self) -> str:
        return self.item

    def get_charges(self) -> int:
        return self.charges
