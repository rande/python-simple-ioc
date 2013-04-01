import ioc.loader, ioc.component, ioc.exceptions
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/redis.yml" % path, container_builder)

        container_builder.parameters.set('ioc.extra.redis.default_connection', config.get('default', 'default'))

        self.configure_connections(config, container_builder)

    def configure_connections(self, config, container_builder):

        manager = container_builder.get('ioc.extra.redis')

        for name, parameters in config.get_dict('connections', {}).all().iteritems():
            id = "ioc.extra.redis.connection.%s" % name
            container_builder.add(id, ioc.component.Definition('redis.ConnectionPool', kwargs={
                'host':             parameters.get('host', 'localhost'),
                'port':             parameters.get_int('port', 6379),
                'db':               parameters.get('db', 0), 
                'password':         parameters.get('password', None),
                'socket_timeout':   parameters.get('socket_timeout', None), 
                'encoding':         parameters.get('encoding', 'utf-8'),
                'encoding_errors':  parameters.get('encoding_errors', 'strict'), 
                'decode_responses': parameters.get('decode_responses', False),
            }))

            manager.add_call('add_connection', arguments=[name, ioc.component.Reference(id)])

        for name, parameters in config.get_dict('clients', {}).all().iteritems():
            id_connection = "ioc.extra.redis.connection.%s" % parameters.get('connection')
            id = "ioc.extra.redis.client.%s" % name

            if not container_builder.has(id_connection):
                raise ioc.exceptions.UnknownService("Redis client defined an undefined service: %s" % id_connection)

            container_builder.add(id, ioc.component.Definition('redis.StrictRedis', kwargs={
                'connection_pool':  ioc.component.Reference(id_connection),
            }))

            manager.add_call('add_client', arguments=[name, ioc.component.Reference(id)])

