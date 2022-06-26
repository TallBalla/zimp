
from .eventFlyweight import EventFlyweight
from .nothingEvent import NothingEvent
from .zombiesEvent import ZombiesEvent
from .itemEvent import ItemEvent
from .healthEvent import HealthEvent


class FlyweightFactory:
    def __init__(self):
        self.events = {}

    def generate_consquence_phrase(self, consquence):
        if consquence is None:
            return 'None'
        try:
            consquence = int(consquence)
        except ValueError:
            return 'text'
        if consquence < 0:
            return 'negative'
        elif consquence > 0:
            return 'positive'
        else:
            return 'equal'

    def generate_key(self, consquence):
        return self.generate_consquence_phrase(consquence) + str(consquence)

    def get_event(self, type, consquence):
        event_key = self.generate_key(consquence)

        if event_key not in self.events:
            self.events[event_key] = eval(f"{type}Event" + "(consquence)")
        return self.events[event_key]
