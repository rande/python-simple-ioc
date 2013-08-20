# vim: set fileencoding=utf-8 :

class Fake(object):
    def __init__(self, mandatory, param=None):
        self.mandatory = mandatory
        self.param = param
        self.ok = True
        self.arg2 = True

    def set_ok(self, ok, arg2=None):
        self.arg2 = arg2
        self.ok = ok

class Foo(object):
    def __init__(self, fake, weak_reference):
        self.fake = fake
        self.weak_reference = weak_reference


class WeakReference(object):
    pass