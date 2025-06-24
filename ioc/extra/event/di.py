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

import ioc.component

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        definition = ioc.component.Definition('ioc.event.Dispatcher', kwargs={
            'logger': ioc.component.Reference('logger')
        })
        container_builder.add('ioc.extra.event_dispatcher', definition)

    def post_build(self, container_builder, container):
        dispatcher = container.get('ioc.extra.event_dispatcher')

        for id in container_builder.get_ids_by_tag('event.listener'):
            definition = container_builder.get(id)
            for option in definition.get_tag('event.listener'):
                if 'name' not in option:
                    break

                if 'method' not in option:
                    break

                if 'priority' not in option:
                    option['priority'] = 0

                if type(option['method']) == str:
                    method = getattr(container.get(id), option['method'])
                else:
                    method = option['method']

                dispatcher.add_listener(option['name'], method, option['priority'])
