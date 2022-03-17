class DevCard():
    def __init__(self, item, event_one, event_two, event_three):
        self.item = item
        self.dev_card_time = {9: event_one,
                              10: event_two,
                              11: event_three}

    def get_card_event(self, time):
        return self.dev_card_time.get(time)

    def get_card_item(self):
        return self.item