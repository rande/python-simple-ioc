# vim: set fileencoding=utf-8 :

import unittest
import ioc.locator
import exceptions, os

current_dir = os.path.dirname(os.path.realpath(__file__))

class TestFilesystemLocator(unittest.TestCase):

    def test_locate_with_fake_path(self):
        locator = ioc.locator.FileSystemLocator('fake')

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.FileSystemLocator(current_dir + "/../fixtures")

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

class TestFunctionLocator(unittest.TestCase):
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

class TestPrefixLocator(unittest.TestCase):
    def test_locate_with_fake_path(self):
        locator = ioc.locator.PrefixLocator({})

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.PrefixLocator({
            "app" : ioc.locator.FileSystemLocator(current_dir + "/../fixtures")
        }, ":")

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('app:services.yml'))

class TestChoiceLocator(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.ChoiceLocator([
            ioc.locator.FileSystemLocator("/tmp"),
            ioc.locator.FileSystemLocator(current_dir + "/../fixtures"),
        ])

        self.assertEquals(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

class TestPackageLocator(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.PackageLocator('tests', 'fixtures')
        self.assertEquals(os.path.realpath(current_dir + "/../fixtures/services.yml"), locator.locate('services.yml'))
