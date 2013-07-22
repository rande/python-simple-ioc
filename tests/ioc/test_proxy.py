# vim: set fileencoding=utf-8 :

import ioc.proxy, ioc.component
import unittest2 as unittest

class FakeService(object):
    p = 42
    def __init__(self):
        self.arg = None

    def method(self):
        return "method"

class ProxyTest(unittest.TestCase):

    def test_support(self):

        fake = FakeService()

        container = ioc.component.Container()
        container.add('fake', fake)

        proxy = ioc.proxy.Proxy(container, 'fake')

        self.assertEquals("method", proxy.method())

        fake.arg = 1

        self.assertEquals(1, proxy.arg)
        self.assertEquals(42, proxy.p)

        self.assertIsInstance(proxy, ioc.proxy.Proxy)
        self.assertIsInstance(proxy, FakeService)