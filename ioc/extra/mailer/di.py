import ioc.loader, ioc.component, ioc.exceptions
import os, datetime

import mailer

class ExtraMailer(mailer.Mailer):
    def create(self, **kwargs):
        return mailer.Message(**kwargs)
        
class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        kwargs = {
            'host': config.get('host', "localhost"),
            'port': config.get('port', 0),
            'use_tls': config.get('use_tls', False),
            'usr': config.get('user', None),
            'pwd': config.get('password', None),
            # 'use_ssl': config.get('use_ssl', False),
        }

        container_builder.add('ioc.extra.mailer', ioc.component.Definition('ioc.extra.mailer.di.ExtraMailer', kwargs=kwargs))

