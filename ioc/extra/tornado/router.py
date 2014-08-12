#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
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

from werkzeug.routing import Map, Rule
import time

class AssetHelper(object):
    def __init__(self, static, router, route_name, version=None):
        self.static = static
        self.version = version or int(time.time())
        self.router = router
        self.route_name = route_name

    def generate_asset(self, path, module=None):
        if not module:
            return self.generate_static(path)

        return self.router.generate(self.route_name, filename=path, module=module, v=self.version)

    def generate_static(self, path):
        """
        This method generates a valid path to the public folder of the running project
        """
        if not path:
            return ""

        if path[0] == '/':
            return "%s?v=%s" % (path, self.version)

        return "%s/%s?v=%s" % (self.static, path, self.version)

class TornadoMultiDict(object):
    """
    This code make the RequestHandler.arguments compatible with WTForm module
    """
    def __init__(self, handler):
        self.handler = handler

    def __iter__(self):
        return iter(self.handler.request.arguments)

    def __len__(self):
        return len(self.handler.request.arguments)

    def __contains__(self, name):
        # We use request.arguments because get_arguments always returns a
        # value regardless of the existence of the key.
        return (name in self.handler.request.arguments)

    def getlist(self, name):
        # get_arguments by default strips whitespace from the input data,
        # so we pass strip=False to stop that in case we need to validate
        # on whitespace.
        return self.handler.get_arguments(name, strip=False)

class Router(object):
    def __init__(self, url_map=None):

        self._url_map = url_map or Map([])
        self._view_functions = {}
        self._adapter = None


    def add(self, name, pattern, view_func, defaults=None, subdomain=None, methods=None,
                 build_only=False, strict_slashes=None,
                 redirect_to=None, alias=False, host=None):

        self._url_map.add(Rule(pattern, endpoint=name, defaults=defaults, subdomain=subdomain, methods=methods,
                              build_only=build_only, strict_slashes=strict_slashes, redirect_to=redirect_to,
                              alias=alias, host=host))

        self._view_functions[name] = view_func

        self._adapter = None

    def bind(self, hostname):
        self._adapter = self._url_map.bind(hostname)

    def adapter(self):
        if not self._adapter:
            self._adapter = self._url_map.bind("localhost")

        return self._adapter

    def match(self, path_info=None, method=None, return_rule=False, query_args=None):
        name, parameters = self.adapter().match(path_info, method, return_rule, query_args)

        return name, parameters, self._view_functions[name]

    def generate(self, name, method=None, force_external=False, append_unknown=True, **kwargs):
        return self.adapter().build(name, kwargs, method, force_external, append_unknown)