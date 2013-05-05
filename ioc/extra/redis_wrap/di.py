import ioc.loader, ioc.component, ioc.exceptions
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        container_builder.parameters.set('ioc.extra.redis_wrap.clients', config.get_dict('clients', {
            'default': 'ioc.extra.redis.client.default' 
        }).all())

    def post_build(self, container_builder, container):
        import redis_wrap

        for name, id in container.parameters.get('ioc.extra.redis_wrap.clients').iteritems():
            redis_wrap.SYSTEMS[name] = container.get(id)