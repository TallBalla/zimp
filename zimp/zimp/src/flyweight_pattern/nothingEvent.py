from .eventFlyweight import EventFlyweight


class NothingEvent(EventFlyweight):
    def __init__(self, consquence):
        super().__init__(type='Nothing', consquence=consquence)
