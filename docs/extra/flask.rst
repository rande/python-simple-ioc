Flask
-----

Flask_ is a web micro framework

Configuration
~~~~~~~~~~~~~

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

Services available
~~~~~~~~~~~~~~~~~~

Services available:

- ioc.extra.flask.app : the Flask app


.. _Flask: http://flask.pocoo.org/
