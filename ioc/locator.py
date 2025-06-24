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

"""
    Resource locator

    This code is based on the jinja2.loaders module
"""
from os import path

class ResourceNotFound(Exception):
    pass

def split_resource_path(resource: str) -> list[str]:
    """Split a path into segments and perform a sanity check.  If it detects
    '..' in the path it will raise a `TemplateNotFound` error.
    """
    pieces = []
    for piece in resource.split('/'):
        if path.sep in piece \
           or (path.altsep and path.altsep in piece) or \
           piece == path.pardir:
            raise ResourceNotFound(resource)
        elif piece and piece != '.':
            pieces.append(piece)
    return pieces


class BaseLocator(object):
    def locate(self, resource: str) -> str:
        raise ResourceNotFound(resource)


class FileSystemLocator(BaseLocator):
    """Locale a ressource from the file system.  This Locator can find ressources
    in folders on the file system and is the preferred way to load them.

    The Locator takes the path to the resource as string, or if multiple
    locations are wanted a list of them which is then looked up in the
    given order:

    >>> locator = FileSystemLocator('/path/to/templates')
    >>> locator = FileSystemLocator(['/path/to/templates', '/other/path'])

    """

    def __init__(self, searchpath):
        if isinstance(searchpath, str):
            searchpath = [searchpath]

        self.searchpath = list(searchpath)

    def locate(self, resource):
        pieces = split_resource_path(resource)
        for searchpath in self.searchpath:
            filename = path.join(searchpath, *pieces)

            if not path.exists(filename):
                continue

            return filename

        raise ResourceNotFound(resource)


class PackageLocator(BaseLocator):
    """Load ressource from python eggs or packages.  It is constructed with
    the name of the python package and the path to the resource folder in that
    package::

        locator = PackageLocator('mypackage', 'views')

    If the package path is not given, ``'resources'`` is assumed.
    """

    def __init__(self, package_name: str, package_path: str = 'resources') -> None:
        try:
            # Python 3.9+
            from importlib import resources
            self.resources = resources
        except ImportError:
            # Fallback for older Python versions
            import importlib_resources as resources
            self.resources = resources
        
        self.package_name = package_name
        self.package_path = package_path

    def locate(self, resource: str) -> str:
        pieces = split_resource_path(resource)
        
        try:
            # Try to access the resource
            package = self.resources.files(self.package_name)
            if self.package_path:
                package = package / self.package_path
            
            for piece in pieces:
                package = package / piece
            
            if not package.is_file():
                raise ResourceNotFound(resource)
            
            # For Python 3.9+, we need to handle the path properly
            if hasattr(package, '__fspath__'):
                return str(package)
            else:
                # Use as_file context manager for temporary access
                with self.resources.as_file(package) as path:
                    return str(path)
        except (AttributeError, FileNotFoundError, ModuleNotFoundError):
            raise ResourceNotFound(resource)

class FunctionLocator(BaseLocator):
    """A locator that is passed a function which does the searching.  The
    function becomes the name of the resource passed and has to return
    a string with the resource sourc.

    >>> def load_resource(name):
    ...     if name == 'index.html':
    ...         return '...'
    ...
    >>> locator = FunctionLocator(load_resource)
    """

    def __init__(self, load_func):
        self.load_func = load_func

    def locate(self, resource):
        rv = self.load_func(resource)
        if rv is None:
            raise ResourceNotFound(resource)

        return rv

class PrefixLocator(BaseLocator):
    """A locator that is passed a dict of locators where each Locator is bound
    to a prefix.  The prefix is delimited from the resource by a slash per
    default, which can be changed by setting the `delimiter` argument to
    something else::

        Locator = PrefixLocator({
            'app1':     PackageLocator('mypackage.app1'),
            'app2':     PackageLocator('mypackage.app2')
        })

    By loading ``'app1/index.html'`` the file from the app1 package is loaded,
    by loading ``'app2/index.html'`` the file from the second.
    """

    def __init__(self, mapping, delimiter='/'):
        self.mapping = mapping
        self.delimiter = delimiter

    def locate(self, resource):
        try:
            prefix, name = resource.split(self.delimiter, 1)
            locator = self.mapping[prefix]
        except (ValueError, KeyError):
            raise ResourceNotFound(resource)

        try:
            return locator.locate(name)
        except ResourceNotFound:
            # re-raise the exception with the correct fileame here.
            # (the one that includes the prefix)
            raise ResourceNotFound(resource)

class ChoiceLocator(BaseLocator):
    """This locator works like the `PrefixLocator` just that no prefix is
    specified.  If a resource could not be found by one locator the next one
    is tried.

    >>> locator = ChoiceLocator([
    ...     FileSystemLocator('/path/to/user/templates'),
    ...     FileSystemLocator('/path/to/system/templates')
    ... ])

    This is useful if you want to allow users to override builtin resources
    from a different location.
    """
    def __init__(self, locators):
        self.locators = locators

    def locate(self, resource):
        for locator in self.locators:
            try:
                return locator.locate(resource)
            except ResourceNotFound:
                pass

        raise ResourceNotFound(resource)
