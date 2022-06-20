from .eventFlyweight import EventFlyweight


class ItemEvent(EventFlyweight):
    def __init__(self, consquence):
        super().__init__(type='Item', consquence=consquence)
