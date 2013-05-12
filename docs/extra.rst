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

        config: # use to populate the instance_relative_config kwargs
            DEBUG:                         False
            TESTING:                       False
            PROPAGATE_EXCEPTIONS:          
            PRESERVE_CONTEXT_ON_EXCEPTION: 
            SECRET_KEY:                    
            USE_X_SENDFILE:                False
            LOGGER_NAME:                   
            SERVER_NAME:                   
            APPLICATION_ROOT:              
            SESSION_COOKIE_NAME:           'session'
            SESSION_COOKIE_DOMAIN:         
            SESSION_COOKIE_PATH:           
            SESSION_COOKIE_HTTPONLY:       True
            SESSION_COOKIE_SECURE:         False
            MAX_CONTENT_LENGTH:            
            SEND_FILE_MAX_AGE_DEFAULT:     43200
            TRAP_BAD_REQUEST_ERRORS:       False
            TRAP_HTTP_EXCEPTIONS:          False
            PREFERRED_URL_SCHEME:          'http'
            JSON_AS_ASCII:                 True

        blueprints:
            - element.flask.blueprint
            

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


redis_wrap
--------

redis-wrap_ implements a wrapper for Redis datatypes so they mimic the datatypes found in Python

.. code-block:: yaml

    ioc.extra.redis_wrap:
        clients:
            default: ioc.extra.redis.client.default

Twisted
-------

Twisted_ is an event-driven networking engine written.

.. code-block:: yaml

    ioc.extra.twisted:

Services available:

- ioc.extra.twisted.reactor: the reactor instance
- ioc.extra.twisted.reactor.thread_pool: the reactor thread pool


Event Dispatcher
----------------

The IoC package includes a small event dispatcher, you can include it by adding this yaml.

.. code-block:: yaml

    ioc.extra.event:

Mailer
------

.. code-block:: yaml

    ioc.extra.mailer:
        host: localhost
        port:
        use_tls: false
        user: 
        password: 
        use_ssl: false


.. _Flask: http://flask.pocoo.org/
.. _Redis-Py: https://github.com/andymccurdy/redis-py
.. _Redis: http://redis.io/
.. _Twisted: http://twistedmatrix.com/
.. _Mailer: https://pypi.python.org/pypi/mailer