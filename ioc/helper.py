# vim: set fileencoding=utf-8 :

import ioc.component
import ioc.loader
import logging

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

class Dict(object):
    def __init__(self, data):
        self.data = data

    def get(self, name, default=None):
        data = self.data
        for name in name.split("."):
            if name in data:
                data = data[name]

            else:
                return default

        return data

def build(files, logger=None):

    if not logger:
        logger = logging.getLogger('ioc')

    container_builder = ioc.component.ContainerBuilder(logger=logger)
    
    loaders = [
        ioc.loader.YamlLoader()
    ]

    logger.debug("Loading files")
    for file in files:
        logger.debug("Search loader for file %s" % file)
        for loader in loaders:
            if not loader.support(file):
                continue

            logger.debug("Found loader %s for file %s" % (loader, file))
            loader.load(file, container_builder)

    container = ioc.component.Container()

    container_builder.build_container(container)

    return container