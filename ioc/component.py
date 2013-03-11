import ioc.exceptions

class Reference(object):
    def __init__(self, id):
        self.id = id
        
class Definition(object):
    def __init__(self, clazz=None, arguments={}, kwargs={}):
        self.clazz = clazz
        self.arguments = arguments
        self.kwargs = kwargs
        self.method_calls = []

class ParameterHolder(object):
    def __init__(self, parameters={}):
        self.parameters = parameters

    def __setitem__(self, key, value):
        self.parameters[key] = value

    def __getitem__(self, key):
        return self.parameters[key]

    def __delitem__(self, key):
        del self.parameters[key]

class ParameterResolver(object):
    def resolve(self, parameter, parameter_holder):
        pass

class Container(object):
    def __init__(self):
        self.services = {}
        self.parameters = ParameterHolder()

    def add(self, id, service):
        self.services[id] = service

    def get(self, id):
        if id not in self.services:
            raise ioc.exceptions.UnknownService()

        return self.services[id]

class ContainerBuilder(Container):
    pass
    # def get_container(self, container, parameter_resolver):
        



