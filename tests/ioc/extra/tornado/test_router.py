import unittest

from ioc.extra.tornado.router import Router

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
        self.assertEquals("/blog/hello", self.router.generate("blog_post", slug="hello"))

        self.assertEquals("http://localhost/blog/hello", self.router.generate("blog_post", slug="hello", force_external=True))