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
import ioc.event

class EventTest(unittest.TestCase):
    def test_init(self):
        event = ioc.event.Event({'foo': 'bar'})
        self.assertEqual('bar', event.get('foo'))

        with self.assertRaises(KeyError):
            self.assertEqual('bar', event.get('foo2'))

        self.assertFalse(event.has('foo2'))

        event.set('foo2', 'bar')
        self.assertTrue(event.has('foo2'))
        self.assertEqual('bar', event.get('foo2'))

    def test_stop_propagation(self):
        event = ioc.event.Event()

        self.assertFalse(event.is_propagation_stop())
        event.stop_propagation()
        self.assertTrue(event.is_propagation_stop())

def mylistener(event):
    event.set('enter', True)

class EventDispatcherTest(unittest.TestCase):
    def test_init(self):
        ioc.event.Dispatcher()

    def test_listener(self):
        dispatcher = ioc.event.Dispatcher()
        dispatcher.add_listener('node.load', mylistener)

        event = dispatcher.dispatch('node.load', {
            'node': {}
        })

        self.assertIsInstance(event, ioc.event.Event)
        self.assertTrue(event.has('node'))
        self.assertTrue(event.has('enter'))
        self.assertTrue(event.get('enter'))

    def test_remove_listener(self):
        dispatcher = ioc.event.Dispatcher()
        dispatcher.add_listener('node.load', mylistener)
        dispatcher.remove_listeners('node.load')

        event = dispatcher.dispatch('node.load', {
            'node': {}
        })

        self.assertFalse(event.has('enter'))

    def test_get_listener(self):
        listeners = [
            ('event32', 32),
            ('event0', 0),
            ('event1', 1),
            ('event-1', -1)
        ]

        dispatcher = ioc.event.Dispatcher()

        for listener, priority in listeners:
            dispatcher.add_listener('node.load', listener, priority)

        expected = ['event32', 'event1', 'event0', 'event-1']

        self.assertEqual(expected, dispatcher.get_listeners('node.load'))

        
