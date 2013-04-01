import exceptions

class Manager(object):
    def __init__(self, default=None, connections=None, clients=None):
        self.connections = connections or {}
        self.clients = clients or {}
        self.default = default or False

    def add_connection(self, name, connection):
        self.connections[name] = connection

    def get_connection(self, name=None):
        if len(self.connections) == 1:
            return self.connections.values()[0]

        if name in self.connections:
            return self.connections[name]

        raise exceptions.KeyError('Unable to find the the valid connection')

    def add_client(self, name, client):
        self.clients[name] = client

    def get_default_client(self):
        if len(self.clients) == 1:
            return self.clients.values()[0]

        if not self.default:
            raise exceptions.KeyError('No default client set')

        return self.get_client(self, self.default)
        
    def get_client(self, name=None):
        if not name:
            return self.get_default_client()

        if name in self.clients:
            return self.clients[name]

        raise exceptions.KeyError('Unable to find the the valid connection')