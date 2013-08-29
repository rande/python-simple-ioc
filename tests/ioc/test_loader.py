# vim: set fileencoding=utf-8 :

import os
import ioc.loader, ioc.component
import unittest2 as unittest

current_dir = os.path.dirname(os.path.realpath(__file__))

class YamlLoaderTest(unittest.TestCase):

    def test_support(self):
        loader = ioc.loader.YamlLoader()

        self.assertTrue(loader.support('foo.yml'))
        self.assertFalse(loader.support('foo.xml'))

    def test_load(self):
        builder = ioc.component.ContainerBuilder()

        loader = ioc.loader.YamlLoader()
        loader.load("%s/../fixtures/services.yml" % current_dir, builder)

        self.assertEquals(5, len(builder.services))
        self.assertTrue('foo' in builder.services)
        self.assertTrue('fake' in builder.services)

        self.assertIsInstance(builder.get('foo'), ioc.component.Definition)
        self.assertIsInstance(builder.get('fake'), ioc.component.Definition)
        self.assertIsInstance(builder.get('foo').arguments[0], ioc.component.Reference)

        self.assertEquals(2, len(builder.get('fake').method_calls))

        self.assertEquals('set_ok', builder.get('fake').method_calls[0][0])
        self.assertEquals([False], builder.get('fake').method_calls[0][1])
        self.assertEquals({}, builder.get('fake').method_calls[0][2])

        self.assertEquals('set_ok', builder.get('fake').method_calls[1][0])
        self.assertEquals([True], builder.get('fake').method_calls[1][1])
        self.assertEquals({'arg2': 'arg'}, builder.get('fake').method_calls[1][2])

        # test tags
        self.assertEquals(['foo'], builder.get_ids_by_tag('jinja.filter'))

    def test_reference(self):
        loader = ioc.loader.YamlLoader()
        
        arguments = ['@fake', ['@hello', '#@weak_reference'], 1]
        
        loader.set_references(arguments)

        self.assertIsInstance(arguments[0], ioc.component.Reference)
        self.assertIsInstance(arguments[1][0], ioc.component.Reference)
        self.assertIsInstance(arguments[1][1], ioc.component.WeakReference)
        self.assertEquals(arguments[2], 1)

        arguments = {'fake': '@hello', 'boo': ['@fake']}

        arguments = loader.set_references(arguments)

        self.assertIsInstance(arguments['fake'], ioc.component.Reference)
        self.assertIsInstance(arguments['boo'][0], ioc.component.Reference)

        self.assertEquals(arguments['fake'].id, 'hello')

    def test_reference_method(self):
        builder = ioc.component.ContainerBuilder()

        loader = ioc.loader.YamlLoader()
        loader.load("%s/../fixtures/services.yml" % current_dir, builder)

        definition = builder.get('method_reference')

        self.assertIsInstance(definition, ioc.component.Definition)
        self.assertIsInstance(definition.arguments[0], ioc.component.Reference)
        self.assertEquals("fake", definition.arguments[0].id)
        self.assertEquals("set_ok", definition.arguments[0].method)
    
    def test_abstract_service(self):
        builder = ioc.component.ContainerBuilder()

        loader = ioc.loader.YamlLoader()
        loader.load("%s/../fixtures/services.yml" % current_dir, builder)

        self.assertTrue(builder.get('abstract_service').abstract)
        self.assertFalse(builder.get('fake').abstract)

