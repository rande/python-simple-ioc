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

import ioc.proxy, ioc.component
import unittest

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

        self.assertEqual("method", proxy.method())

        fake.arg = 1

        self.assertEqual(1, proxy.arg)
        self.assertEqual(42, proxy.p)

        self.assertIsInstance(proxy, ioc.proxy.Proxy)
        self.assertIsInstance(proxy, FakeService)
