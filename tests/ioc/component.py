# vim: set fileencoding=utf-8 :

import unittest
import ioc.component, ioc.exceptions, exceptions
import tests.ioc.service

class TestDefinition(unittest.TestCase):
    def test_init(self):
        definition = ioc.component.Definition()
        self.assertIsNone(definition.klass)
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

    def test_parameters(self):
        holder = ioc.component.ParameterHolder()
        holder['bonjour'] = 'hello'
        holder['le_monde'] = 'world'

        parameter_resolver = ioc.component.ParameterResolver()
        
        self.assertEquals("hello", parameter_resolver.resolve("%bonjour%", holder))
        self.assertEquals("hello world", parameter_resolver.resolve("%bonjour% %le_monde%", holder))
        self.assertEquals(['hello world', 'hello world'], parameter_resolver.resolve(["%bonjour% %le_monde%", "%bonjour% %le_monde%"], holder))        

    def test_parameters(self):
        holder = ioc.component.ParameterHolder()
        parameter_resolver = ioc.component.ParameterResolver()
        
        self.assertEquals(1, parameter_resolver.resolve(1, holder))
        self.assertEquals(1.0, parameter_resolver.resolve(1.0, holder))
        self.assertEquals(True, parameter_resolver.resolve(True, holder))
        

    def test_escaping(self):
        holder = ioc.component.ParameterHolder()
        holder['bonjour'] = 'hello'
        holder['le_monde'] = 'world'

        parameter_resolver = ioc.component.ParameterResolver()

        self.assertEquals("%hello", parameter_resolver.resolve("%%%bonjour%", holder))
        self.assertEquals("%hello world %", parameter_resolver.resolve("%%%bonjour% %le_monde% %", holder))

        # Recurive parameters ?? => not now
        # holder['foo'] = 'bar'
        # holder['baz'] = '%%%foo% %foo%%% %%foo%% %%%foo%%%'
        # self.assertEquals("%%bar bar%% %%foo%% %%bar%%", parameter_resolver.resolve('%baz%', holder))


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

class TestContainerBuilder(unittest.TestCase):
    def setUp(self):
        self.container = ioc.component.ContainerBuilder()

    def test_get_class(self):
        with self.assertRaises(exceptions.AttributeError):
            self.container.get_class(ioc.component.Definition('tests.ioc.component.Fake'))

        definition = ioc.component.Definition('tests.ioc.service.Fake', [True], {'param': 'salut'})

        c = self.container.get_class(definition)
        
        self.assertEquals(c.__name__, tests.ioc.service.Fake.__name__)


    def test_get_instance(self):
        definition = ioc.component.Definition('tests.ioc.service.Fake', [True], {'param': 'salut'})
        container = ioc.component.Container()

        c = self.container.get_class(definition)
        i = self.container.get_instance(c, definition, container)

        self.assertIs(type(i), tests.ioc.service.Fake)
        self.assertEquals(True, i.mandatory)
        self.assertEquals('salut', i.param)

    def test_get_container(self):        
        self.container.add('service.id.1', ioc.component.Definition('tests.ioc.service.Fake', [True], {'param': 'salut'}))
        self.container.add('service.id.2', ioc.component.Definition('tests.ioc.service.Fake', [False], {'param': 'hello'}))
        self.container.add('service.id.3', ioc.component.Definition('tests.ioc.service.Foo', [ioc.component.Reference('service.id.2')]))

        container = ioc.component.Container()

        self.container.build_container(container)

        self.assertEquals(3, len(container.services))
        self.assertTrue(container.has('service.id.2'))
        self.assertIsInstance(container.get('service.id.2'), tests.ioc.service.Fake)
        self.assertIsInstance(container.get('service.id.3'), tests.ioc.service.Foo)

        self.assertEquals(container.get('service.id.3').fake, container.get('service.id.2'))

    def test_cyclic_reference(self):
        self.container.add('service.id.1', ioc.component.Definition('tests.ioc.service.Foo', [ioc.component.Reference('service.id.1')]))

        container = ioc.component.Container()
        parameter_resolver = ioc.component.ParameterResolver()

        with self.assertRaises(ioc.exceptions.CyclicReference):
            self.container.build_container(container)

        