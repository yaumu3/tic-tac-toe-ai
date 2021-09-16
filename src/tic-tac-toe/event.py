class Event:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def trigger(self, **kwargs):
        for listener in self.listeners:
            listener(**kwargs)
