__author__ = 'rande'

class JinjaHelper(object):
    def __init__(self, container):
        self.container = container

    def get_parameter(self, name, default=None):
        if self.container.parameters.has(name):
            return self.container.parameters.get(name)

        return default