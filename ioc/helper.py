#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
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

import ioc.component
import ioc.loader
import logging

def deepcopy(value):
    """
    The default copy.deepcopy seems to copy all objects and some are not
    `copy-able`.

    We only need to make sure the provided data is a copy per key, object does
    not need to be copied.
    """

    if not isinstance(value, (dict, list, tuple)):
        return value

    if isinstance(value, dict):
        copy = {}
        for k, v in value.items():
            copy[k] = deepcopy(v)

    if isinstance(value, tuple):
        copy = list(range(len(value)))

        for k in get_keys(list(value)):
            copy[k] = deepcopy(value[k])

        copy = tuple(copy)

    if isinstance(value, list):
        copy = list(range(len(value)))

        for k in get_keys(value):
            copy[k] = deepcopy(value[k])

    return copy

def is_scalar(value):
    return isinstance(value, (str))

def is_iterable(value):
    return isinstance(value, (dict, list))

def get_keys(arguments):
    if isinstance(arguments, (list)):
        return range(len(arguments))

    if isinstance(arguments, (dict)):
        return arguments.keys()

    return []

class Dict(object):
    def __init__(self, data=None):
        self.data = data or {}

    def get(self, name, default=None):
        data = self.data
        for name in name.split("."):
            if name in data:
                data = data[name]

            else:
                return default

        return data

    def get_dict(self, name, default=None):
        default = default or {}
        value = self.get(name, default)

        if not isinstance(value, Dict):
            value = Dict(value)

        return value

    def get_int(self, name, default=None):
        return int(self.get(name, default))

    def get_all(self, name, default=None):
        return self.get_dict(name, default).all()

    def all(self):
        def walk(data):
            all = {}

            if not isinstance(data, dict):
                return data

            for v, d in data.iteritems():
                if isinstance(d, Dict):
                    all[v] = d.all()
                else:
                    all[v] = d

                if is_iterable(all[v]):
                    walk(all[v])

            return all

        return walk(self.data)

    def iteritems(self):
        return self.data.iteritems()

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

def build(files, logger=None, parameters=None):

    if not logger:
        logger = logging.getLogger('ioc')

    if not parameters:
        parameters = {
            'ioc.debug': False
        }

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

    for name, value in parameters.items():
        container_builder.parameters.set(name, value)

    container_builder.build_container(container)

    return container