import os
import ioc.loader, ioc.component
import unittest

current_dir = os.path.dirname(os.path.realpath(__file__))

class TestYamlLoader(unittest.TestCase):

    def test_support(self):
        loader = ioc.loader.YamlLoader()

        self.assertTrue(loader.support('foo.yml'))
        self.assertFalse(loader.support('foo.xml'))

    def test_load(self):
        builder = ioc.component.ContainerBuilder()

        loader = ioc.loader.YamlLoader()
        loader.load("%s/../fixtures/services.yml" % current_dir, builder)

        self.assertEquals(2, len(builder.services))
        self.assertTrue('foo' in builder.services)
        self.assertTrue('fake' in builder.services)

        self.assertIsInstance(builder.get('foo'), ioc.component.Definition)
        self.assertIsInstance(builder.get('fake'), ioc.component.Definition)
        self.assertEquals(['@fake'], builder.get('foo').arguments)

    def test_reference(self):

        loader = ioc.loader.YamlLoader()
        
        arguments = ['@fake', ['@hello']]
        
        loader.set_references(arguments)

        self.assertIsInstance(arguments[0], ioc.component.Reference)
        self.assertIsInstance(arguments[1][0], ioc.component.Reference)

        arguments = {'fake': '@hello', 'boo': ['@fake']}

        arguments = loader.set_references(arguments)

        self.assertIsInstance(arguments['fake'], ioc.component.Reference)
        self.assertIsInstance(arguments['boo'][0], ioc.component.Reference)

        self.assertEquals(arguments['fake'].id, 'hello')