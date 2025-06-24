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

import ioc.loader, ioc.component
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/command.yml" % path, container_builder)

    def post_build(self, container_builder, container):
        command_manager = container.get('ioc.extra.command.manager')

        for id in container_builder.get_ids_by_tag('command'):
            definition = container_builder.get(id)
            for option in definition.get_tag('command'):
                if 'name' not in option:
                    break

                command_manager.add_command(option['name'], container.get(id))
