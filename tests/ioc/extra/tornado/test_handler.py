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

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from ioc.event import Dispatcher

from ioc.extra.tornado.router import Router
from ioc.extra.tornado.handler import RouterHandler


def view(handler, name=None):
    handler.write("Hello %s" % name)

def error(handler):
    raise Exception()

class MyHTTPTest(AsyncHTTPTestCase):
    def get_app(self):

        dispatcher = Dispatcher()

        def error_listener(event):
            event.get('request_handler').write('An unexpected error occurred')

        def not_found_listener(event):
            event.get('request_handler').write('Not Found')

        dispatcher.add_listener('handler.not_found', not_found_listener)
        dispatcher.add_listener('handler.exception', error_listener)

        router = Router()
        router.add("hello", "/hello/<string:name>", view, methods=['GET'])
        router.add("exception", "/exception", error, methods=['GET'])

        return Application([("/.*", RouterHandler, dict(router=router, event_dispatcher=dispatcher))])

    def test_not_found(self):
        response = self.fetch('/')
        self.assertEquals("Not Found", response.body)
        self.assertEquals(404, response.code)

    def test_found(self):
        response = self.fetch('/hello/Thomas')
        self.assertEquals("Hello Thomas", response.body)
        self.assertEquals(200, response.code)

    def test_error(self):
        response = self.fetch('/exception')

        self.assertEquals("An unexpected error occurred", response.body[0:28])
        self.assertEquals(500, response.code)
