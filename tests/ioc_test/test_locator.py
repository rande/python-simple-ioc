#
# Copyright 2014-2025 Thomas Rabaix <thomas.rabaix@gmail.com>
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
import ioc.locator
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

class FilesystemLocatorTest(unittest.TestCase):

    def test_locate_with_fake_path(self):
        locator = ioc.locator.FileSystemLocator('fake')

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.FileSystemLocator(current_dir + "/../fixtures")

        self.assertEqual(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

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

        self.assertEqual("/mypath/services.yml", locator.locate('services.yml'))

class PrefixLocatorTest(unittest.TestCase):
    def test_locate_with_fake_path(self):
        locator = ioc.locator.PrefixLocator({})

        with self.assertRaises(ioc.locator.ResourceNotFound):
            locator.locate('missing file')

    def test_locate(self):
        locator = ioc.locator.PrefixLocator({
            "app" : ioc.locator.FileSystemLocator(current_dir + "/../fixtures")
        }, ":")

        self.assertEqual(current_dir + "/../fixtures/services.yml", locator.locate('app:services.yml'))

class ChoiceLocatorTest(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.ChoiceLocator([
            ioc.locator.FileSystemLocator("/tmp"),
            ioc.locator.FileSystemLocator(current_dir + "/../fixtures"),
        ])

        self.assertEqual(current_dir + "/../fixtures/services.yml", locator.locate('services.yml'))

class PackageLocatorTest(unittest.TestCase):
    def test_locate(self):
        locator = ioc.locator.PackageLocator('tests', 'fixtures')
        self.assertEqual(os.path.realpath(current_dir + "/../fixtures/services.yml"), locator.locate('services.yml'))
