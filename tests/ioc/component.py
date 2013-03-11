import unittest
import ioc.component, ioc.exceptions

class TestDefinition(unittest.TestCase):
    def test_init(self):
        definition = ioc.component.Definition()

        self.assertIsNone(definition.clazz)
        self.assertEquals(0, len(definition.arguments))

class TestParameterHolder(unittest.TestCase):
    def test_init(self):
        parameter_holder = ioc.component.ParameterHolder()

        self.assertEquals(0, len(parameter_holder.parameters))

    def test_item(self):
        parameter_holder = ioc.component.ParameterHolder()
        
        parameter_holder['foo'] = 'bar'

        self.assertEquals(1, len(parameter_holder.parameters))

        self.assertEquals('bar', parameter_holder['foo'])
        del parameter_holder['foo']

        self.assertEquals(0, len(parameter_holder.parameters))
        
class TestParameterResolver(unittest.TestCase):
    def test_init(self):
        parameter_resolver = ioc.component.ParameterResolver()


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = ioc.component.Container()

    def test_add(self):
        self.container.add('myid', {})
        self.container.add('myid', {})
        self.container.add('myid.2', {})

        self.assertEquals(2, len(self.container.services));

    def test_get(self):
        self.container.add('myid', {})
        self.assertEquals({}, self.container.get('myid'))

        with self.assertRaises(ioc.exceptions.UnknownService):
            self.container.get('fake')