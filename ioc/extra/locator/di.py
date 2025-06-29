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

import ioc.loader, ioc.component, ioc.exceptions
from ioc.component import Definition

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        extensions = container_builder.parameters.get('ioc.extensions')

        locator_map = {}

        for extension in extensions:
            arguments = [[
                Definition('ioc.locator.FileSystemLocator', arguments=["%s/resources/%s" % (container_builder.parameters.get('project.root_folder'), extension)]),
                Definition('ioc.locator.PackageLocator', arguments=[extension], kwargs={'package_path': 'resources'}),
                Definition('ioc.locator.PackageLocator', arguments=[extension], kwargs={'package_path': ''})
            ]]
            
            locator_map[extension] = Definition('ioc.locator.ChoiceLocator', arguments=arguments)

        container_builder.add('ioc.locator', Definition('ioc.locator.PrefixLocator', arguments=[locator_map], kwargs={'delimiter': ':'}))
