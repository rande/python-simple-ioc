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
        router = Router()
        router.add("hello", "/hello/<string:name>", view, methods=['GET'])
        router.add("exception", "/exception", error, methods=['GET'])

        return Application([("/.*", RouterHandler, dict(router=router, event_dispatcher=Dispatcher()))])

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
