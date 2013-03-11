# vim: set fileencoding=utf-8 :

import yaml

from ioc.component import Definition, Reference
import ioc.helper

class YamlLoader(object):
    def support(self, file):
        return file[-3:] == 'yml'

    def load(self, file, container_builder):
        data = yaml.load(open(file).read())

        if 'parameters' in data:
            for key, value in data['parameters'].iteritems():
                container_builder.parameters[key] = value

        if 'services' in data:
            for id, meta in data['services'].iteritems():

                if 'arguments' not in meta:
                    meta['arguments'] = []

                if 'class' not in meta:
                    meta['class'] = None

                if 'kwargs' not in meta:
                    meta['kwargs'] = {}

                definition = Definition(
                    clazz=meta['class'], 
                    arguments=self.set_references(meta['arguments']), 
                    kwargs=self.set_references(meta['kwargs'])
                )

                container_builder.add(id, definition)

    def set_reference(self, value):
        if ioc.helper.is_scalar(value) and value[0:1] == '@':
            return Reference(value[1:])

        if ioc.helper.is_iterable(value):
            return self.set_references(value)

        return value

    def set_references(self, arguments):
        for pos in ioc.helper.get_keys(arguments):
            arguments[pos] = self.set_reference(arguments[pos])

        return arguments