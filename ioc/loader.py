import yaml

from ioc.component import Definition, Reference

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
                    arguments=meta['arguments'], 
                    kwargs=meta['kwargs']
                )

                container_builder.add(id, definition)

    def is_scalar(self, value):
        return isinstance(value, (str))

    def is_iterable(self, value):
        return isinstance(value, (dict, list))

    def set_reference(self, value):
        if self.is_scalar(value) and value[0:1] == '@':
            return Reference(value[1:])

        if self.is_iterable(value):
            return self.set_references(value)

    def get_keys(self, arguments):
        if isinstance(arguments, (list)):
            return range(len(arguments))

        if isinstance(arguments, (dict)):
            return arguments.iterkeys()

    def set_references(self, arguments):
        for pos in self.get_keys(arguments):
            arguments[pos] = self.set_reference(arguments[pos])

        return arguments