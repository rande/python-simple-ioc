# vim: set fileencoding=utf-8 :

import unittest2 as unittest
import ioc.event
import exceptions

class EventTest(unittest.TestCase):
    def test_init(self):
        event = ioc.event.Event({'foo': 'bar'})
        self.assertEquals('bar', event.get('foo'))

        with self.assertRaises(exceptions.KeyError):
            self.assertEquals('bar', event.get('foo2'))

        self.assertFalse(event.has('foo2'))

        event.set('foo2', 'bar')
        self.assertTrue(event.has('foo2'))
        self.assertEquals('bar', event.get('foo2'))


    def test_stop_propagation(self):
        event = ioc.event.Event()

        self.assertFalse(event.is_propagation_stop())
        event.stop_propagation()
        self.assertTrue(event.is_propagation_stop())

def mylistener(event):
    event.set('enter', True)

class EventTest(unittest.TestCase):
    def test_init(self):
        dispatcher = ioc.event.Dispatcher()

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
