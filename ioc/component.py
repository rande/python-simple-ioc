# vim: set fileencoding=utf-8 :

import ioc.exceptions, ioc.helper
from ioc.proxy import Proxy

import importlib, inspect, re

class Extension(object):
    def load(self, config, container_builder):
        pass

    def post_load(self, container_builder):
        pass

    def pre_build(self, container_builder, container):
        pass

    def post_build(self, container_builder, container):
        pass

    def start(self, container):
        pass

class Reference(object):
    def __init__(self, id, method=None):
        self.id = id
        self.method = method

class WeakReference(Reference):
    pass

class Definition(object):
    def __init__(self, clazz=None, arguments=None, kwargs=None, abstract=False):
        self.clazz = clazz
        self.arguments = arguments or [] 
        self.kwargs = kwargs or {}
        self.method_calls = []
        self.property_calls = []
        self.tags = {}
        self.abstract = abstract

    def add_call(self, method, arguments=None, kwargs=None):
        self.method_calls.append([
            method,
            arguments or [],
            kwargs or {}
        ])

    def add_tag(self, name, options=None):
        if name not in self.tags:
            self.tags[name] = []

        self.tags[name].append(options or {})

    def has_tag(self, name):
        return name in self.tags

    def get_tag(self, name):
        if not self.has_tag(name):
            return []

        return self.tags[name]

class ParameterHolder(object):
    def __init__(self, parameters=None):
        self._parameters = parameters or {}
        self._frozen = False

    def set(self, key, value):
        if self._frozen:
            raise ioc.exceptions.ParameterHolderIsFrozen(key)

        self._parameters[key] = value

    def get(self, key):
        if key in self._parameters:
            return self._parameters[key]

        raise ioc.exceptions.UnknownParameter(key)

    def remove(self, key):
        del self._parameters[key]

    def has(self, key):
        return key in self._parameters

    def all(self):
        return self._parameters

    def freeze(self):
        self._frozen = True

    def is_frozen(self):
        return self._frozen == True

class ParameterResolver(object):
    def __init__(self, logger=None):
        self.re = re.compile("%%|%([^%\s]+)%")
        self.logger = logger
        self.stack = []

    def _resolve(self, parameter, parameter_holder):
        if isinstance(parameter, (tuple)):
            parameter = list(parameter)
            for key in ioc.helper.get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

            return tuple(parameter)

        if ioc.helper.is_iterable(parameter):
            for key in ioc.helper.get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

            return parameter

        if not type(parameter) == str:
            return parameter

        if parameter[0:1] == '%' and parameter[-1] == '%' and parameter_holder.has(parameter[1:-1]):
            # if self.logger:
            #     self.logger.debug("   >> Match parameter: %s" % parameter[1:-1])

            return self.resolve(parameter_holder.get(parameter[1:-1]), parameter_holder)


        def replace(matchobj):
            if matchobj.group(0) == '%%':
                return '%'

            return self.resolve(parameter_holder.get(matchobj.group(1)), parameter_holder)

        # if self.logger:
        #     self.logger.debug("   >> Start resolving parameter: %s" % parameter)

        parameter, nums = re.subn(self.re, replace, parameter)

        # print parameter
        return parameter

    def resolve(self, parameter, parameter_holder):
        if parameter in self.stack:
            raise ioc.exceptions.RecursiveParameterResolutionError(" -> ".join(self.stack) + " -> " + parameter)

        parameter = ioc.helper.deepcopy(parameter)

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

    def get_ids_by_tag(self, name):
        return [id for id, definition in self.services.iteritems() if definition.has_tag(name)]

    def build_container(self, container):
        if self.logger:
            self.logger.debug("Start building the container")

        extensions = []
        container.add("service_container", container)
        self.parameters.set('ioc.extensions', self.extensions.keys())

        for name, config in self.extensions.iteritems():
            name = "%s.di.Extension" % name

            if self.logger:
                self.logger.debug("Load extension %s" % name)

            extension = self.get_class(Definition(name))()
            extension.load(config, self)

            extensions.append(extension)

        for extension in extensions:
            extension.post_load(self)

        for extension in extensions:
            extension.pre_build(self, container)

        # resolve services
        for id, definition in self.services.iteritems():
            if definition.abstract:
                continue

            self.get_service(id, definition, container)

        for extension in extensions:
            extension.post_build(self, container)

        if self.logger:
            self.logger.debug("Building container is over!")
            self.logger.debug("Starting resolving all parameters!")

        for name, value in self.parameters.all().iteritems():
            container.parameters.set(
                name, 
                self.parameter_resolver.resolve(value, self.parameters)
            )

        if self.logger:
            self.logger.debug("End resolving all parameters!")

        if container.has('ioc.extra.event_dispatcher'):
            container.get('ioc.extra.event_dispatcher').dispatch('ioc.container.built', {
                'container': container,
                'container_builder': self
            })

        return container

    def create_definition(self, id):
        abstract = self.services[id]

        definition = Definition(
            clazz=abstract.clazz, 
            arguments=ioc.helper.deepcopy(abstract.arguments),
            kwargs=ioc.helper.deepcopy(abstract.kwargs),
            abstract=False,
        )

        definition.method_calls = ioc.helper.deepcopy(abstract.method_calls)
        definition.property_calls = ioc.helper.deepcopy(abstract.property_calls)
        definition.tags = ioc.helper.deepcopy(abstract.tags)

        return definition

    def get_class(self, definition):
        clazz = self.parameter_resolver.resolve(definition.clazz, self.parameters)

        if isinstance(clazz, list):
            module = clazz[0]
            function = clazz[1]
        else:
            module = ".".join(clazz.split(".")[0:-1])
            function = clazz.split(".")[-1]

        module = importlib.import_module(module)

        function = function.split(".")
        clazz = getattr(module, function[0])

        if len(function) == 2:
            return getattr(clazz, function[1])

        return clazz

    def get_instance(self, definition, container):

        klass = self.get_class(definition)

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

            attr = getattr(instance, method)

            if not attr:
                # handle property definition
                setattr(instance, method, self.set_services(args, container)[0])
            else:
                attr(*self.set_services(args, container), **self.set_services(kwargs, container))
            
        if self.logger:
            self.logger.debug("End creating instance %s" % instance)

        return instance

    def get_service(self, id, definition, container):

        if self.logger:
            self.logger.debug("Get service: id=%s, class=%s" % (id, definition.clazz))

        if definition.abstract:
            raise ioc.exceptions.AbstractDefinitionInitialization("The ContainerBuiler try to build an abstract definition, id=%s, class=%s" % (id, definition.clazz))

        if container.has(id):
            return container.get(id)

        if id in self.stack:
            if self.logger:
                self.logger.error("ioc.exceptions.CyclicReference: " + " -> ".join(self.stack) + " -> " + id)

            raise ioc.exceptions.CyclicReference(" -> ".join(self.stack) + " -> " + id)

        self.stack.append(id)
        instance = self.get_instance(definition, container)
        container.add(id, instance)
        self.stack.pop()

        return instance

    def retrieve_service(self, value, container):
        if isinstance(value, (Reference, WeakReference)) and not container.has(value.id) and not self.has(value.id):
            raise ioc.exceptions.UnknownService(value.id)

        if isinstance(value, (Reference)):
            if not container.has(value.id):
                service = self.get_service(value.id, self.get(value.id), container)
            else:
                service = container.get(value.id)

            # a reference can point a service's method, and not the service itself...
            if value.method:
                return getattr(service, value.method)

            return service

        if isinstance(value, (WeakReference)):
            # if the container already has the service return the service and not the proxy
            if not container.has(value.id):
                return Proxy(container, value.id)

            return container.get(value.id)

        if isinstance(value, Definition):
            return self.get_instance(value, container)

        if ioc.helper.is_iterable(value):
            return self.set_services(value, container)

        if isinstance(value, (tuple)):
            return tuple(self.set_services(list(value), container))

        return self.parameter_resolver.resolve(value, self.parameters)

    def set_services(self, arguments, container):
        for pos in ioc.helper.get_keys(arguments):
            arguments[pos] = self.retrieve_service(arguments[pos], container)

        return arguments
