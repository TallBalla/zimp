class Event():
    def __init__(self, event_prop, event_desc):
        self.event_prop = event_prop
        self.event_desc = event_desc

    def get_event_prop(self):
        return self.event_prop

    def get_event_desc(self):
        return self.event_desc
