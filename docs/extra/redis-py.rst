Redis-Py
--------

Redis-Py_ is an interface to the Redis_ key-value store.

Configuration
~~~~~~~~~~~~~

.. code-block:: yaml

    ioc.extra.redis:
        clients:
            default:
                connection: default

        connections:
            default:
                host:               'localhost'
                port:               6379
                db:                 0
                password:
                socket_timeout:
                encoding:           'utf-8'
                encoding_errors:    'strict'
                decode_responses:   false

Services available
~~~~~~~~~~~~~~~~~~


- ioc.extra.redis.manager: the Redis manager to retrieve client and connection
- ioc.extra.redis.connection.default: the ``default`` connection
- ioc.extra.redis.client.default: the ``default`` client


.. _Redis-Py: https://github.com/andymccurdy/redis-py
.. _Redis: http://redis.io/
