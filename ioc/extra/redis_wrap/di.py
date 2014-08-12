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

import ioc.loader, ioc.component, ioc.exceptions

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        container_builder.parameters.set('ioc.extra.redis_wrap.clients', config.get_dict('clients', {
            'default': 'ioc.extra.redis.client.default' 
        }).all())

    def post_build(self, container_builder, container):
        import redis_wrap

        for name, id in container.parameters.get('ioc.extra.redis_wrap.clients').items():
            redis_wrap.SYSTEMS[name] = container.get(id)