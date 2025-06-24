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

from typing import Any, Optional
import ioc.component
import ioc.loader
import logging

def build(files: list[str], logger: Optional[logging.Logger] = None, parameters: Optional[dict[str, Any]] = None) -> Any:

    if not logger:
        logger = logging.getLogger('ioc')

    if not parameters:
        parameters = {
            'ioc.debug': False
        }

    container_builder = ioc.component.ContainerBuilder(logger=logger)
        
    loaders = [
        ioc.loader.YamlLoader()
    ]

    logger.debug("Loading files")

    for file in files:
        logger.debug("Search loader for file %s" % file)
        for loader in loaders:
            if not loader.support(file):
                continue

            logger.debug("Found loader %s for file %s" % (loader, file))

            loader.load(file, container_builder)

    container = ioc.component.Container()

    for name, value in parameters.items():
        container_builder.parameters.set(name, value)

    container_builder.build_container(container)

    return container
