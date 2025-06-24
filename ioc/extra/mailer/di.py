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

from ioc.component import Definition, Extension

import mailer

class ExtraMailer(mailer.Mailer):
    def create(self, **kwargs):
        return mailer.Message(**kwargs)

class Extension(Extension):
    def load(self, config, container_builder):
        kwargs = {
            'host': config.get('host', "localhost"),
            'port': config.get('port', 0),
            'use_tls': config.get('use_tls', False),
            'usr': config.get('user', None),
            'pwd': config.get('password', None),
            # 'use_ssl': config.get('use_ssl', False),
        }

        container_builder.add('ioc.extra.mailer', Definition('ioc.extra.mailer.di.ExtraMailer', kwargs=kwargs))
