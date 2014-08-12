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

import yaml, collections

from ioc.component import Definition, Reference, WeakReference
import ioc.helper, ioc.exceptions
from .misc import OrderedDictYAMLLoader

class Loader(object):
    def fix_config(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                config[key] = self.fix_config(value)

        return ioc.helper.Dict(config)

class YamlLoader(Loader):
    def support(self, file):
        return file[-3:] == 'yml'

    def load(self, file, container_builder):

        try:
            data = yaml.load(open(file).read(), OrderedDictYAMLLoader)
        except yaml.scanner.ScannerError as e:
            raise ioc.exceptions.LoadingError("file %s, \nerror: %s" % (file, e))

        for extension, config in data.items():
            if extension in ['parameters', 'services']:
                continue

            if config == None:
                config = {}

            container_builder.add_extension(extension, self.fix_config(config.copy()))

        if 'parameters' in data:
            for key, value in data['parameters'].items():
                container_builder.parameters.set(key, value)

        if 'services' in data:
            for id, meta in data['services'].items():

                if 'arguments' not in meta:
                    meta['arguments'] = []

                if 'class' not in meta:
                    meta['class'] = None

                if 'kwargs' not in meta:
                    meta['kwargs'] = {}

                if 'calls' not in meta:
                    meta['calls'] = []

                if 'tags' not in meta:
                    meta['tags'] = {}

                if 'abstract' not in meta:
                    meta['abstract'] = False

                definition = Definition(
                    clazz=meta['class'], 
                    arguments=self.set_references(meta['arguments']), 
                    kwargs=self.set_references(meta['kwargs']),
                    abstract=meta['abstract']
                )

                for call in meta['calls']:
                    if len(call) == 0:
                        continue

                    if len(call) == 2:
                        call.append({})

                    if len(call) == 1:
                        call.append([])
                        call.append({})

                    definition.method_calls.append(
                        (call[0], self.set_references(call[1]), self.set_references(call[2]))
                    )

                for tag, options in meta['tags'].items():
                    for option in options:
                        definition.add_tag(tag, option)

                container_builder.add(id, definition)

    def set_reference(self, value):
        if ioc.helper.is_scalar(value) and value[0:1] == '@':
            if '#' in value:
                id, method = value.split("#")
                return Reference(id[1:], method)

            return Reference(value[1:])

        if ioc.helper.is_scalar(value) and value[0:2] == '#@':
            return WeakReference(value[2:])

        if ioc.helper.is_iterable(value):
            return self.set_references(value)

        return value

    def set_references(self, arguments):
        for pos in ioc.helper.get_keys(arguments):
            arguments[pos] = self.set_reference(arguments[pos])

        return arguments