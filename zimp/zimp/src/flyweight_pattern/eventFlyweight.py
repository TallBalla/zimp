from abc import ABC, abstractmethod


class EventFlyweight(ABC):
    def __init__(self, type, consquence):
        self.type = type
        self.consquence = consquence

    def get_type(self):
        return self.type

    def get_consquence(self):
        return self.consquence
