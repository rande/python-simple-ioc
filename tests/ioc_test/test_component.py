#
# Copyright 2014-2025 Thomas Rabaix <thomas.rabaix@gmail.com>
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

import unittest
import ioc.component, ioc.exceptions
import tests.ioc_test.service

class DefinitionTest(unittest.TestCase):
    def test_init(self):
        definition = ioc.component.Definition()
        self.assertIsNone(definition.clazz)
        self.assertEqual(0, len(definition.arguments))

    def test_tag(self):
        definition = ioc.component.Definition()
        definition.add_tag('jinja.filter')

        self.assertFalse(definition.has_tag('salut'))
        self.assertTrue(definition.has_tag('jinja.filter'))

        self.assertEqual([{}], definition.get_tag('jinja.filter'))

class ParameterHolderTest(unittest.TestCase):
    def test_init(self):
        parameter_holder = ioc.component.ParameterHolder()

        self.assertEqual(0, len(parameter_holder.all()))

    def test_item(self):
        parameter_holder = ioc.component.ParameterHolder()
        
        parameter_holder.set('foo', 'bar')

        self.assertEqual(1, len(parameter_holder.all()))

        self.assertEqual('bar', parameter_holder.get('foo'))
        parameter_holder.remove('foo')

        self.assertEqual(0, len(parameter_holder.all()))

    def test_missing_parameter(self):

        parameter_holder = ioc.component.ParameterHolder()

        with self.assertRaises(ioc.exceptions.UnknownParameter):
            parameter_holder.get('error')
        
class ParameterResolverTest(unittest.TestCase):
    def test_init(self):
        ioc.component.ParameterResolver()

    def test_parameters(self):
        holder = ioc.component.ParameterHolder()
        holder['bonjour'] = 'hello'
        holder['le_monde'] = 'world'

        parameter_resolver = ioc.component.ParameterResolver()
        
        self.assertEqual("hello", parameter_resolver.resolve("%bonjour%", holder))
        self.assertEqual("hello world", parameter_resolver.resolve("%bonjour% %le_monde%", holder))
        self.assertEqual(['hello world', 'hello world'], parameter_resolver.resolve(["%bonjour% %le_monde%", "%bonjour% %le_monde%"], holder))        

    def test_parameter_types(self):
        holder = ioc.component.ParameterHolder()
        parameter_resolver = ioc.component.ParameterResolver()
        
        self.assertEqual(1, parameter_resolver.resolve(1, holder))
        self.assertEqual(1.0, parameter_resolver.resolve(1.0, holder))
        self.assertEqual(True, parameter_resolver.resolve(True, holder))
    
    def test_replace_array(self):
        holder = ioc.component.ParameterHolder()
        holder.set('array', [4, 2])

        parameter_resolver = ioc.component.ParameterResolver()

        self.assertEqual([4, 2], parameter_resolver.resolve("%array%", holder))

    def test_replace_tuple(self):
        holder = ioc.component.ParameterHolder()
        holder.set('tuple', "salut")

        parameter_resolver = ioc.component.ParameterResolver()

        self.assertEqual(("salut", 2), parameter_resolver.resolve(("%tuple%", 2), holder))

    def test_escaping(self):
        holder = ioc.component.ParameterHolder()
        holder.set('bonjour', 'hello')
        holder.set('le_monde', 'world')

        parameter_resolver = ioc.component.ParameterResolver()

        self.assertEqual("%hello", parameter_resolver.resolve("%%%bonjour%", holder))
        self.assertEqual("%hello world %", parameter_resolver.resolve("%%%bonjour% %le_monde% %", holder))

        # Recurive parameters ?? => not now
        # holder['foo'] = 'bar'
        # holder['baz'] = '%%%foo% %foo%%% %%foo%% %%%foo%%%'
        # self.assertEqual("%%bar bar%% %%foo%% %%bar%%", parameter_resolver.resolve('%baz%', holder))

    def test_nested_parameters(self):
        holder = ioc.component.ParameterHolder()
        holder.set('bonjour', 'hello')
        holder.set('le_monde', 'world %exclamation%')
        holder.set('exclamation', '!')

        parameter_resolver = ioc.component.ParameterResolver()

        self.assertEqual("hello world !", parameter_resolver.resolve("%bonjour% %le_monde%", holder))

    def test_nested_parameters_recursive(self):
        holder = ioc.component.ParameterHolder()
        holder.set('bonjour', 'hello %le_monde%')
        holder.set('le_monde', '%bonjour% world')

        parameter_resolver = ioc.component.ParameterResolver()

        with self.assertRaises(ioc.exceptions.RecursiveParameterResolutionError):
            parameter_resolver.resolve("%bonjour% %le_monde%", holder)


class ContainerTest(unittest.TestCase):
    def setUp(self):
        self.container = ioc.component.Container()

    def test_add(self):
        self.container.add('myid', {})
        self.container.add('myid', {})
        self.container.add('myid.2', {})

        self.assertEqual(2, len(self.container.services))

    def test_get(self):
        self.container.add('myid', {})
        self.assertEqual({}, self.container.get('myid'))

        with self.assertRaises(ioc.exceptions.UnknownService):
            self.container.get('fake')

class ContainerBuilderTest(unittest.TestCase):
    def setUp(self):
        self.container = ioc.component.ContainerBuilder()

    def test_get_class(self):
        with self.assertRaises(AttributeError):
            self.container.get_class(ioc.component.Definition('tests.ioc_test.test_component.Fake'))

        definition = ioc.component.Definition('tests.ioc_test.service.Fake', [True], {'param': 'salut'})

        c = self.container.get_class(definition)
        
        self.assertEqual(c.__name__, tests.ioc_test.service.Fake.__name__)

    def test_get_instance(self):
        definition = ioc.component.Definition('tests.ioc_test.service.Fake', [True], {'param': 'salut'})
        container = ioc.component.Container()

        i = self.container.get_instance(definition, container)

        self.assertIs(type(i), tests.ioc_test.service.Fake)
        self.assertEqual(True, i.mandatory)
        self.assertEqual('salut', i.param)

    def test_get_container(self):        
        self.container.add('service.id.1', ioc.component.Definition('tests.ioc_test.service.Fake', [True], {'param': 'salut'}))
        self.container.add('service.id.2', ioc.component.Definition('tests.ioc_test.service.Fake', [False], {'param': 'hello'}))
        self.container.add('service.id.3', ioc.component.Definition('tests.ioc_test.service.Foo', [ioc.component.Reference('service.id.2'), None]))

        container = ioc.component.Container()

        self.container.build_container(container)

        self.assertEqual(5, len(container.services))
        self.assertTrue(container.has('service.id.2'))
        self.assertIsInstance(container.get('service.id.2'), tests.ioc_test.service.Fake)
        self.assertIsInstance(container.get('service.id.3'), tests.ioc_test.service.Foo)

        self.assertEqual(container.get('service.id.3').fake, container.get('service.id.2'))

    def test_cyclic_reference(self):
        self.container.add('service.id.1', ioc.component.Definition('tests.ioc_test.service.Foo', [ioc.component.Reference('service.id.1'), None]))

        container = ioc.component.Container()
        
        with self.assertRaises(ioc.exceptions.CyclicReference):
            self.container.build_container(container)

    def test_get_ids_by_tag(self):
        definition = ioc.component.Definition('tests.ioc_test.service.Foo')
        definition.add_tag('jinja.filter')
        self.container.add('service.id.1', definition)

        self.assertEqual([], self.container.get_ids_by_tag('non_existent_tag'))
        self.assertEqual(['service.id.1'], self.container.get_ids_by_tag('jinja.filter'))

    def test_definition_with_inner_definition(self):

        definition = ioc.component.Definition('tests.ioc_test.service.Fake', arguments=[
            ioc.component.Definition('tests.ioc_test.service.Fake', arguments=[
                ioc.component.Definition('tests.ioc_test.service.Fake', arguments=[1])
            ])
        ])

        self.container.add('foo', definition)

        container = ioc.component.Container()
        self.container.build_container(container)

        self.assertIsInstance(container.get('foo'), tests.ioc_test.service.Fake)
        self.assertIsInstance(container.get('foo').mandatory, tests.ioc_test.service.Fake)
        self.assertIsInstance(container.get('foo').mandatory.mandatory, tests.ioc_test.service.Fake)
        
    def test_reference_with_method(self):
        self.container.add('service.id.1', ioc.component.Definition('tests.ioc_test.service.Fake', [ioc.component.Reference('service.id.2', 'set_ok')]))
        self.container.add('service.id.2', ioc.component.Definition('tests.ioc_test.service.Fake', ['foo']))

        container = ioc.component.Container()

        self.container.build_container(container)

        self.assertEqual(container.get('service.id.1').mandatory, container.get('service.id.2').set_ok)

    def test_exception_for_abstract_definition(self):
        definition = ioc.component.Definition('tests.ioc_test.service.Fake', ['foo'], abstract=True)

        container = ioc.component.Container()

        with self.assertRaises(ioc.exceptions.AbstractDefinitionInitialization):
            self.container.get_service("foo", definition, container)

    def test_abstracted_service_not_in_the_container(self):
        definition = ioc.component.Definition('tests.ioc_test.service.Fake', ['foo'], abstract=True)

        self.container.add('service.id.abstract', definition)

        container = ioc.component.Container()

        self.container.build_container(container)

        self.assertEqual(2, len(container.services))

    def test_create_definition_from_abstract_definition(self):
        self.container.add('service.id.abstract', ioc.component.Definition('tests.ioc_test.service.Fake', ['foo'], abstract=True))

        definition = self.container.create_definition('service.id.abstract')

        self.container.add('service.id.1', definition)

        container = self.container.build_container(ioc.component.Container())
        self.assertEqual(3, len(container.services))
