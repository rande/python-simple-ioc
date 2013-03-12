# vim: set fileencoding=utf-8 :

import ioc.component
import ioc.loader

def is_scalar(value):
    return isinstance(value, (str))

def is_iterable(value):
    return isinstance(value, (dict, list))

def get_keys(arguments):
    if isinstance(arguments, (list)):
        return range(len(arguments))

    if isinstance(arguments, (dict)):
        return arguments.iterkeys()

    return []

def build(files):
    container_builder = ioc.component.ContainerBuilder()
    
    loaders = [
        ioc.loader.YamlLoader()
    ]

    for file in files:
        for loader in loaders:
            if not loader.support(file):
                continue

            loader.load(file, container_builder)

    parameter_resolver = ioc.component.ParameterResolver()
    
    container = ioc.component.Container()
    container_builder.build_container(container, parameter_resolver)

    return container