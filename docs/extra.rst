Extra
=====

The ioc package include some integration with python lib, just edit the ``config.yml`` file and add the different following ``yaml`` sections.

Flask
-----

Flask_ is a web micro framework

.. code-block:: yaml

    ioc.extra.flask:
        app:
            port:               8080
            name:               ''
            static_path:        ''
            static_url_path:    ''
            static_folder:      'static'
            template_folder:    'templates'
            instance_path:      ''
            instance_relative_config: false

Services available:

- ioc.extra.flask.app : the Flask app


Redis-Py
--------

Redis-Py_ is an interface to the Redis_ key-value store.

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

Services available:

- ioc.extra.redis.manager: the Redis manager to retrieve client and connection
- ioc.extra.redis.connection.default: the ``default`` connection
- ioc.extra.redis.client.default: the ``default`` client


Twisted
-------

Twisted_ is an event-driven networking engine written.

.. code-block:: yaml

    ioc.extra.twisted:

Services available:

- ioc.extra.twisted.reactor: the reactor instance
- ioc.extra.twisted.reactor.thread_pool: the reactor thread pool


.. _Flask: http://flask.pocoo.org/
.. _Redis-Py: https://github.com/andymccurdy/redis-py
.. _Redis: http://redis.io/
.. _Twisted: http://twistedmatrix.com/