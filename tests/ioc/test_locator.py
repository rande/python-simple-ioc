# vim: set fileencoding=utf-8 :

import unittest2 as unittest
import ioc.locator
import exceptions, os

current_dir = os.path.dirname(os.path.realpath(__file__))

class FilesystemLocatorTest(unittest.TestCase):

    def test_locate_with_fake_path(self):
        locator = ioc.locator.FileSystemLocator('fake')

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.FileSystemLocator(current_dir + "/../fixtures")

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

class FunctionLocatorTest(unittest.TestCase):
    def test_locate_with_fake_path(self):
        def function(resource):
            return None

        locator = ioc.locator.FunctionLocator(function)

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        def function(resource):
            return "/mypath/%s" % resource

        locator = ioc.locator.FunctionLocator(function)

        self.assertEquals("/mypath/services.yml", locator.locate('services.yml'))

class PrefixLocatorTest(unittest.TestCase):
    def test_locate_with_fake_path(self):
        locator = ioc.locator.PrefixLocator({})

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.PrefixLocator({
            "app" : ioc.locator.FileSystemLocator(current_dir + "/../fixtures")
        }, ":")

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('app:services.yml'))

class ChoiceLocatorTest(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.ChoiceLocator([
            ioc.locator.FileSystemLocator("/tmp"),
            ioc.locator.FileSystemLocator(current_dir + "/../fixtures"),
        ])

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

class PackageLocatorTest(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.PackageLocator('tests', 'fixtures')
        self.assertEquals(os.path.realpath(current_dir + "/../fixtures/services.yml"), locator.locate('services.yml'))
