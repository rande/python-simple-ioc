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

from ioc.extra.jinja2.helper import JinjaHelper
from ioc.component import Container
class JinjaHelperTest(unittest.TestCase):
    def test_get_parameter(self):

        container = Container()
        container.parameters.set('hello', 'world')

        helper = JinjaHelper(container)

        self.assertEqual('world', helper.get_parameter('hello'))
        self.assertEqual(None, helper.get_parameter('fake'))
        self.assertEqual('for real', helper.get_parameter('fake', 'for real'))
