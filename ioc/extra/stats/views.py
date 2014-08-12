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

from element.node import NodeHandler

class IndexView(object):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context):

        return 200, 'ioc.extra.stats:index.html', {}

class ParametersView(NodeHandler):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context, type=None):

        params = {
            'parameters': self.container.parameters,
            'context': context
        }

        return self.render(request_handler, self.container.get('ioc.extra.jinja2'), 'ioc.extra.stats:parameters.html', params)

class ServicesView(NodeHandler):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context):
        context.node.title = "Services"

        return 200, 'ioc.extra.stats:services.html', {
            'services': self.container.services,
            'context': context,
        }
