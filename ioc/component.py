# vim: set fileencoding=utf-8 :

import ioc.exceptions, ioc.helper
import re, exceptions
import importlib, inspect
from ioc.proxy import Proxy


class Extension(object):
    def load(self, config, container_builder):
        pass

    def post_load(self, container_builder, container):
        pass

    def pre_build(self, container_builder, container):
        pass

    def post_build(self, container):
        pass

    def start(self, container):
        pass

class Reference(object):
    def __init__(self, id):
        self.id = id

class WeakReference(Reference):
    pass

class Definition(object):
    def __init__(self, clazz=None, arguments={}, kwargs={}):
        self.module = None
        self.function = None

        if clazz:
            if isinstance(clazz, list):
                self.module = clazz[0]
                self.function = clazz[1]
            else:
                self.module = ".".join(clazz.split(".")[0:-1])
                self.function = clazz.split(".")[-1]

        self.arguments = arguments
        self.kwargs = kwargs
        self.method_calls = []

class ParameterHolder(object):
    def __init__(self, parameters={}):
        self.parameters = parameters

    def set(self, key, value):
        self.parameters[key] = value

    def get(self, key):
        if key in self.parameters:
            return self.parameters[key]

        raise ioc.exceptions.UnknownParameter(key)

    def remove(self, key):
        del self.parameters[key]

    def has(self, key):
        return key in self.parameters

class ParameterResolver(object):
    def __init__(self, logger=None):
        self.re = re.compile("%%|%([^%\s]+)%")
        self.logger = logger
        self.stack = []

    def _resolve(self, parameter, parameter_holder):
        if not type(parameter) == str:
            return parameter

        if ioc.helper.is_iterable(parameter):
            for key in ioc.helper.get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

        elif parameter[0:1] == '%' and parameter[-1] == '%' and parameter_holder.has(parameter[1:-1]):
            if self.logger:
                self.logger.debug("   >> Match parameter: %s" % parameter[1:-1])

            return self.resolve(parameter_holder.get(parameter[1:-1]), parameter_holder)

        else:
            def replace(matchobj):
                if matchobj.group(0) == '%%':
                    return '%'

                return self.resolve(parameter_holder.get(matchobj.group(1)), parameter_holder)

            if self.logger:
                self.logger.debug("   >> Start resolving parameter: %s" % parameter)

            parameter, nums = re.subn(self.re, replace, parameter)

        return parameter

    def resolve(self, parameter, parameter_holder):
        if parameter in self.stack:
            raise ioc.exceptions.RecursiveParameterResolutionError(" -> ".join(self.stack) + " -> " + parameter)

        self.stack.append(parameter)
        value = self._resolve(parameter, parameter_holder)
        self.stack.pop()

        return value

class Container(object):
    def __init__(self):
        self.services = {}
        self.parameters = ParameterHolder()
        self.stack = []

    def has(self, id):
        return id in self.services

    def add(self, id, service):
        self.services[id] = service

    def get(self, id):
        if id not in self.services:
            raise ioc.exceptions.UnknownService(id)

        return self.services[id]

class ContainerBuilder(Container):
    def __init__(self, logger=None):
        self.services = {}
        self.parameters = ParameterHolder()
        self.stack = []
        self.logger = logger
        self.parameter_resolver = ioc.component.ParameterResolver(logger=logger)
        self.extensions = {}

    def add_extension(self, name, config):
        self.extensions[name] = config

    def build_container(self, container):
        if self.logger:
            self.logger.debug("Start building the container")

        extensions = []

        for name, config in self.extensions.iteritems():
            name = "%s.di.Extension" % name

            if self.logger:
                self.logger.debug("Load extension %s" % name)

            extension = self.get_class(Definition(name))()
            extension.load(config, self)

            extensions.append(extension)

        container.add("service_container", container)

        for extension in extensions:
            extension.post_load(self, container)

        for extension in extensions:
            extension.pre_build(self, container)

        for id, definition in self.services.iteritems():
            self.get_service(id, definition, container)

        for extension in extensions:
            extension.post_build(container)

        if self.logger:
            self.logger.debug("Building container is over!")

        # start ....
        # @todo: start a threaded pool

    def get_class(self, definition):
        m = importlib.import_module(definition.module)

        f = definition.function.split(".")
        clazz = getattr(m, f[0])

        if len(f) == 2:
            return getattr(clazz, f[1])

        return clazz

    def get_instance(self, klass, definition, container):

        if self.logger:
            self.logger.debug("Create instance for %s" % klass)

        if inspect.isclass(klass) or inspect.isfunction(klass) or inspect.ismethod(klass):
            args = self.set_services(definition.arguments, container)
            kwargs = self.set_services(definition.kwargs, container)

            instance = klass(*args, **kwargs)
        else:
            # module object ...
            instance = klass

        for call in definition.method_calls:
            method, args, kwargs = call

            if self.logger:
                self.logger.debug(" > Call method: %s on class: %s" % (method, instance))

            getattr(instance, method)(*self.set_services(args, container), **self.set_services(kwargs, container))

        if self.logger:
            self.logger.debug("End creating instance %s" % instance)

        return instance

    def get_service(self, id, definition, container):

        if self.logger:
            self.logger.debug("Get service: id=%s, module=%s, function=%s" % (id, definition.module, definition.function))

        if container.has(id):
            return container.get(id)

        if id in self.stack:
            if self.logger:
                self.logger.error("ioc.exceptions.CyclicReference: " + " -> ".join(self.stack) + " -> " + id)

            raise ioc.exceptions.CyclicReference(" -> ".join(self.stack) + " -> " + id)

        self.stack.append(id)
        instance = self.get_instance(self.get_class(definition), definition, container)
        container.add(id, instance)
        self.stack.pop()

        return instance

    def set_service(self, value, container):
        if isinstance(value, (Reference, WeakReference)) and not self.has(value.id):
            raise ioc.exceptions.UnknownService(value.id)

        if isinstance(value, WeakReference) and not container.has(value.id):
            return Proxy(container, value.id)

        if isinstance(value, Reference) and not container.has(value.id):
            return self.get_service(value.id, self.get(value.id), container)

        if isinstance(value, Reference) and container.has(value.id):
            return container.get(value.id)

        if ioc.helper.is_iterable(value):
            return self.set_services(value, container)

        return self.parameter_resolver.resolve(value, self.parameters)

    def set_services(self, arguments, container):
        for pos in ioc.helper.get_keys(arguments):
            arguments[pos] = self.set_service(arguments[pos], container)

        return arguments
