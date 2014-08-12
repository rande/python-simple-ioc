#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
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

from ioc.extra.tornado.router import Router, TornadoMultiDict
from tornado.httpserver import HTTPRequest
import wtforms

def view():
    return "hello"

class RouterTest(unittest.TestCase):
    def setUp(self):

        self.router = Router()

    def test_add_and_match_routes(self):
        self.router.add("homepage", "/", view)

        self.assertEquals(('homepage', {}, view), self.router.match("/"))

        self.router.add("blog_post", "/blog/<string:slug>", view, methods=['GET'])

        self.assertEquals(('blog_post', {'slug': 'hello'}, view), self.router.match("/blog/hello"))

    def test_add_and_generate_routes(self):

        self.router.add("homepage", "/", view)
        self.router.add("blog_post", "/blog/<string:slug>", view)

        self.assertEquals("/", self.router.generate("homepage"))
        self.assertEquals("/?panel=user", self.router.generate("homepage", panel="user"))
        self.assertEquals("/blog/hello", self.router.generate("blog_post", slug="hello"))

        self.assertEquals("http://localhost/blog/hello", self.router.generate("blog_post", slug="hello", force_external=True))
