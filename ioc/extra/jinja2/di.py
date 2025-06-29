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
import importlib
import jinja2

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/jinja.yml" % path, container_builder)

        # register template
        # retrieve all extensions and build a valid MapPrefixLoader dict
        mapping = {}
        for name, config in container_builder.extensions.items():
            mapping[name] = jinja2.FileSystemLoader([
                "%s/resources/%s/templates" % (container_builder.parameters.get('project.root_folder'), name),
                "%s/resources/templates" % os.path.dirname(importlib.import_module(name).__file__),
                "%s/templates" % os.path.dirname(importlib.import_module(name).__file__),
            ])

        container_builder.parameters.set("ioc.extra.jinja2.loader_mapping", mapping)

    def post_build(self, container_builder, container):
        """
        Register filter and global in jinja environment instance

        IoC tags are:
            - jinja2.filter to register filter, the tag must contain
            a name and a method options
            - jinja2.global to add new global, here globals are functions. 
            The tag must contain a name and a method options
        """
        jinja = container.get('ioc.extra.jinja2')

        for id in container_builder.get_ids_by_tag('jinja2.filter'):
            definition = container_builder.get(id)
            for option in definition.get_tag('jinja2.filter'):
                if 'name' not in option:
                    break

                if 'method' not in option:
                    break

                jinja.filters[option['name']] = getattr(container.get(id), option['method'])

        for id in container_builder.get_ids_by_tag('jinja2.global'):
            definition = container_builder.get(id)
            for option in definition.get_tag('jinja2.global'):

                if 'name' not in option:
                    break

                if 'method' not in option:
                    break                

                jinja.globals[option['name']] = getattr(container.get(id), option['method'])
