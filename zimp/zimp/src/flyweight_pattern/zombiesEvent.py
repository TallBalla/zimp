from .eventFlyweight import EventFlyweight


class ZombiesEvent(EventFlyweight):
    def __init__(self, consquence):
        super().__init__(type='Zombies', consquence=consquence)
