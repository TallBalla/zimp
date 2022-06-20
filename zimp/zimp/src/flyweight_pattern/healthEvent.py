from .eventFlyweight import EventFlyweight


class HealthEvent(EventFlyweight):
    def __init__(self, consquence):
        super().__init__(type='Health', consquence=consquence)