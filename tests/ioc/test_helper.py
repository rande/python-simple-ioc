# vim: set fileencoding=utf-8 :

import ioc
import os
import unittest2 as unittest

current_dir = os.path.dirname(os.path.realpath(__file__))

class HelperTest(unittest.TestCase):

    def test_build(self):
        container = ioc.build([
            "%s/../fixtures/services.yml" % current_dir
        ], parameters={'inline': 'parameter'})

        self.assertEquals(5, len(container.services))
        self.assertEquals(container.get('foo').fake, container.get('fake'))
        self.assertEquals('argument 1', container.get('fake').mandatory)

        self.ok = True
        self.arg2 = True

        fake = container.get('fake')
        self.assertEquals(True, fake.ok)
        self.assertEquals("arg", fake.arg2)

        self.assertTrue(container.get('foo').weak_reference == container.get('weak_reference'))

        self.assertEquals('the argument 1', container.parameters.get('foo.foo'))
        self.assertEquals('parameter', container.parameters.get('inline'))

    def test_dict(self):

        d = ioc.helper.Dict({'key': 'value'})

        self.assertEquals('value', d.get('key'))
        self.assertEquals(None, d.get('key.fake'))
        self.assertEquals('default', d.get('key.fake', 'default'))

        config = ioc.helper.Dict()
        managers = config.get_dict('managers', {'foo': 'bar'})

        self.assertEquals(managers.get('foo'), 'bar')