from werkzeug.routing import Map, Rule

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

    def adapter(self):
        if not self._adapter:
            self._adapter = self._url_map.bind("localhost")

        return self._adapter

    def match(self, path_info=None, method=None, return_rule=False, query_args=None):
        name, parameters = self.adapter().match(path_info, method, return_rule, query_args)

        return name, parameters, self._view_functions[name]

    def generate(self, name, values=None, method=None, force_external=False, append_unknown=True):

        return self.adapter().build(name, values, method, force_external, append_unknown)