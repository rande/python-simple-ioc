class Event(object):
    _propagation_stopped = False

    def __init__(self, data=None):
        self.listeners = {}
        self.data = data or {}

    def stop_propagation(self):
        self._propagation_stopped = True

    def is_propagation_stop(self):
        return self._propagation_stopped

    def get(self, name):
        return self.data[name]

    def set(self, name, value):
        self.data[name] = value

    def has(self, name):
        return name in self.data

class Dispatcher(object):
    
    def __init__(self):
        self.listeners = {}

    def dispatch(self, name, event=None):
        if isinstance(event, dict):
            event = Event(event)

        event = event or Event()

        if name not in self.listeners:
            return event

        for listener in self.listeners[name]:
            listener(event)

            if event.stop_propagation():
                break

        return event

    def add_listener(self, name, listener):
        if name not in self.listeners:
            self.listeners[name] = []

        self.listeners[name].append(listener)

    def remove_listener(self, name, listener):
        if name not in self.listeners:
            return

        self.listeners[name] = [item for item in self.listeners[name] if item != listener]

    def remove_listeners(self, name):
        if name in self.listeners:
            self.listeners[name] = []
