# vim: set fileencoding=utf-8 :

class Fake(object):
    def __init__(self, mandatory, param=None):
        self.mandatory = mandatory
        self.param = param

class Foo(object):
    def __init__(self, fake):
        self.fake