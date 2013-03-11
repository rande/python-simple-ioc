# vim: set fileencoding=utf-8 :

import ioc.exceptions
import importlib

class Reference(object):
    def __init__(self, id):
        self.id = id
        
class Definition(object):
    def __init__(self, clazz=None, arguments={}, kwargs={}):
        self.klass = clazz
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

    def has(self, id):
        return id in self.services
        
    def add(self, id, service):
        self.services[id] = service

    def get(self, id):
        if id not in self.services:
            raise ioc.exceptions.UnknownService()

        return self.services[id]

class ContainerBuilder(Container):
    def build_container(self, container, parameter_resolver):
        for id, definition in self.services.iteritems():
            container.add(id, self.get_service(definition))

    def get_class(self, definition):
        class_name = definition.klass.split(".")[-1]
        module_name = ".".join(definition.klass.split(".")[0:-1])

        m = importlib.import_module(module_name)

        return getattr(m, class_name)

    def get_instance(self, klass, definition):
        return klass(*definition.arguments, **definition.kwargs)

    def get_service(self, definition):
        return self.get_instance(self.get_class(definition), definition)

        
        


        



