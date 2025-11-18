#
# Copyright 2014-2025 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from typing import Any, Optional, Union
from .exceptions import UnknownService, ParameterHolderIsFrozen, UnknownParameter, RecursiveParameterResolutionError, AbstractDefinitionInitialization, CyclicReference
from .proxy import Proxy
from .misc import deepcopy, get_keys, is_iterable

import importlib, inspect, re, logging

HAS_PYDANTIC = False
try:
    from pydantic import BaseModel as PydanticBaseModel
    HAS_PYDANTIC = True
except ImportError:
    pass

class Reference(object):
    def __init__(self, id: str, method: Optional[str] = None) -> None:
        self.id = id
        self.method = method

class WeakReference(Reference):
    pass

class Definition(object):
    def __init__(self, clazz: Optional[Union[str, list[str]]] = None, arguments: Optional[list[Any]] = None, kwargs: Optional[dict[str, Any]] = None, abstract: bool = False) -> None:
        self.clazz = clazz
        self.arguments = arguments or [] 
        self.kwargs = kwargs or {}
        self.method_calls: list[list[Any]] = []
        self.property_calls: list[Any] = []
        self.tags: dict[str, list[dict[str, Any]]] = {}
        self.abstract = abstract

    def add_call(self, method: str, arguments: Optional[list[Any]] = None, kwargs: Optional[dict[str, Any]] = None) -> None:
        self.method_calls.append([
            method,
            arguments or [],
            kwargs or {}
        ])

    def add_tag(self, name: str, options: Optional[dict[str, Any]] = None) -> None:
        if name not in self.tags:
            self.tags[name] = []

        self.tags[name].append(options or {})

    def has_tag(self, name: str) -> bool:
        return name in self.tags

    def get_tag(self, name: str) -> list[dict[str, Any]]:
        if not self.has_tag(name):
            return []

        return self.tags[name]

class ParameterHolder(object):
    def __init__(self, parameters: Optional[dict[str, Any]] = None) -> None:
        self._parameters = parameters or {}
        self._frozen = False

    def set(self, key: str, value: Any) -> None:
        if self._frozen:
            raise ParameterHolderIsFrozen(key)

        self._parameters[key] = value

    def get(self, key: str) -> Any:
        if key in self._parameters:
            return self._parameters[key]

        raise UnknownParameter(key)

    def remove(self, key: str) -> None:
        del self._parameters[key]

    def has(self, key: str) -> bool:
        return key in self._parameters

    def all(self) -> dict[str, Any]:
        return self._parameters

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def freeze(self) -> None:
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen == True

class ParameterResolver(object):
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.re = re.compile(r"%%|%([^%\s]+)%")
        self.logger = logger
        self.stack: list[str] = []

    def _resolve(self, parameter: Any, parameter_holder: ParameterHolder) -> Any:
        if HAS_PYDANTIC and isinstance(parameter, PydanticBaseModel):
            # If the parameter is a Pydantic model, resolve its fields
            def walk_and_modify(model):
                for field in type(model).model_fields:
                    value = getattr(model, field)
                    if isinstance(value, PydanticBaseModel):
                        parameter = walk_and_modify(value)  # Recursive call for nested models
                    else:
                        parameter = self.resolve(value, parameter_holder)

                    setattr(model, field, parameter)

                return model

            return walk_and_modify(parameter)
                
        if isinstance(parameter, (tuple)):
            parameter = list(parameter)
            for key in get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

            return tuple(parameter)

        if is_iterable(parameter):
            for key in get_keys(parameter):
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

    def resolve(self, parameter: Any, parameter_holder: ParameterHolder) -> Any:
        if parameter in self.stack:
            raise RecursiveParameterResolutionError(" -> ".join(self.stack) + " -> " + parameter)

        parameter = deepcopy(parameter)

        self.stack.append(parameter)
        value = self._resolve(parameter, parameter_holder)
        self.stack.pop()

        return value

class Container(object):
    def __init__(self) -> None:
        self.services: dict[str, Any] = {}
        self.parameters = ParameterHolder()
        self.stack: list[str] = []

    def has(self, id: str) -> bool:
        return id in self.services

    def add(self, id: str, service: Any) -> None:
        self.services[id] = service

    def get(self, id: str) -> Any:
        if id not in self.services:
            raise UnknownService(id)

        return self.services[id]

class ContainerBuilder(Container):
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.services: dict[str, Definition] = {}
        self.parameters = ParameterHolder()
        self.stack: list[str] = []
        self.logger = logger
        self.parameter_resolver = ParameterResolver(logger=logger)
        self.extensions: dict[str, Any] = {}

    def add_extension(self, name: str, config: Any) -> None:
        self.extensions[name] = config

    def get_ids_by_tag(self, name: str) -> list[str]:
        return [id for id, definition in self.services.items() if definition.has_tag(name)]

    def build_container(self, container: Container) -> Container:
        if self.logger:
            self.logger.debug("Start building the container")

        extensions = []
        container.add("service_container", container)

        if not container.has('logger'):
            if not self.logger:
                import logging
                container.add("logger", logging.getLogger('app'))
            else:
                container.add("logger", self.logger)

        self.parameters.set('ioc.extensions', self.extensions.keys())

        for name, config in self.extensions.items():
            name = "%s.di.Extension" % name

            if self.logger:
                self.logger.debug("Load extension %s" % name)

            extension = self.get_class(Definition(name))()
            extension.load(config, self)

            extensions.append(extension)

        for extension in extensions:
            extension.post_load(self)

        if self.logger:
            self.logger.debug("Starting resolving all parameters!")
            
        for name, value in self.parameters.all().items():
            container.parameters.set(
                name, 
                self.parameter_resolver.resolve(value, self.parameters)
            )

        if self.logger:
            self.logger.debug("End resolving all parameters!")

        for extension in extensions:
            extension.pre_build(self, container)

        # resolve services
        for id, definition in self.services.items():
            if definition.abstract:
                continue

            self.get_service(id, definition, container)

        for extension in extensions:
            extension.post_build(self, container)

        if self.logger:
            self.logger.debug("Building container is over!")

        if container.has('ioc.extra.event_dispatcher'):
            container.get('ioc.extra.event_dispatcher').dispatch('ioc.container.built', {
                'container': container,
                'container_builder': self
            })

        for extension in extensions:
            extension.start(container)

        return container

    def create_definition(self, id: str) -> Definition:
        abstract = self.services[id]

        definition = Definition(
            clazz=abstract.clazz, 
            arguments=deepcopy(abstract.arguments),
            kwargs=deepcopy(abstract.kwargs),
            abstract=False,
        )

        definition.method_calls = deepcopy(abstract.method_calls)
        definition.property_calls = deepcopy(abstract.property_calls)
        definition.tags = deepcopy(abstract.tags)

        return definition

    def get_class(self, definition: Definition) -> Any:
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

    def get_instance(self, definition: Definition, container: Container) -> Any:

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

    def get_service(self, id: str, definition: Definition, container: Container) -> Any:
        if definition.abstract:
            raise AbstractDefinitionInitialization("The ContainerBuiler try to build an abstract definition, id=%s, class=%s" % (id, definition.clazz))

        if container.has(id):
            return container.get(id)

        if id in self.stack:
            if self.logger:
                self.logger.error("ioc.exceptions.CyclicReference: " + " -> ".join(self.stack) + " -> " + id)

            raise CyclicReference(" -> ".join(self.stack) + " -> " + id)

        self.stack.append(id)
        instance = self.get_instance(definition, container)
        container.add(id, instance)
        self.stack.pop()

        return instance

    def retrieve_service(self, value: Any, container: Container) -> Any:
        if isinstance(value, (Reference, WeakReference)) and not container.has(value.id) and not self.has(value.id):
            raise UnknownService(value.id)

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

        if is_iterable(value):
            return self.set_services(value, container)

        if isinstance(value, (tuple)):
            return tuple(self.set_services(list(value), container))

        return self.parameter_resolver.resolve(value, self.parameters)

    def set_services(self, arguments: Union[list[Any], dict[str, Any]], container: Container) -> Union[list[Any], dict[str, Any]]:
        for pos in get_keys(arguments):
            arguments[pos] = self.retrieve_service(arguments[pos], container)

        return arguments

class Extension(object):
    def load(self, config: Any, container_builder: ContainerBuilder) -> None:
        pass

    def post_load(self, container_builder: ContainerBuilder) -> None:
        pass

    def pre_build(self, container_builder: ContainerBuilder, container: Container) -> None:
        pass

    def post_build(self, container_builder: ContainerBuilder, container: Container) -> None:
        pass

    def start(self, container: Container) -> None:
        pass
