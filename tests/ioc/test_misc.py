# vim: set fileencoding=utf-8 :
from ioc.misc import OrderedDictYAMLLoader

import ioc.proxy, ioc.component
import unittest2 as unittest
import os
import yaml

current_dir = os.path.dirname(os.path.realpath(__file__))

class MiscTest(unittest.TestCase):

    def test_true_as_key(self):

        data = yaml.load(open("%s/../fixtures/order_list.yml" % current_dir).read(), OrderedDictYAMLLoader)

        self.assertEquals(data['list']['true'], 'OK')
