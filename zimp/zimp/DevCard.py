class DevCard:
    def __init__(self,
                 item: str,
                 charges: int,
                 event_one: str,
                 event_two: str,
                 event_three: str):
        self.item = item
        self.charges = charges
        self.event_one = event_one
        self.event_two = event_two
        self.event_three = event_three

        if self.charges != "Unlimited":
            int(self.charges)

    def get_event_at_time(self, time: int) -> str:
        if time == 9:
            return self.event_one
        elif time == 10:
            return self.event_two
        elif time == 11:
            return self.event_three

    def get_item(self) -> str:
        return self.item

    def get_charges(self) -> int:
        return self.charges
