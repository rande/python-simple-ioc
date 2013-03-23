============================================
Python Simple Dependency Injection Container
============================================

This project is a simple port of the Symfony2 DependencyInjection lib available at https://github.com/symfony/DependencyInjection

Status: Work In Progress

Usage
-----

- Services Definition

.. code-block:: yaml

    parameters:
        foo.bar: argument 1

    services:
        fake:
            class: tests.ioc.service.Fake
            arguments: 
                - "%foo.bar%"
            kargs:
                param: here a parameter
            calls:
                 - [ set_ok, [ false ]]
                 - [ set_ok, [ true ], {arg2: "arg"} ]

        foo:
            class: tests.ioc.service.Foo
            arguments: ["@fake", "#@weak_reference"]
            kargs: {}

        weak_reference:
            class: tests.ioc.service.WeakReference


.. code-block:: python

    import ioc

    container = ioc.build(['service.yml'])

    foo = container.get('foo')

Extensions
----------

An extension allows to add new services into the container, the extension is loaded by adding the module name in the configuration file.

For instance, the following code will load the ioc.extra.flask.di.Extension class to add flask app inside the container.

.. code-block:: yaml

    ioc.extra.flask:

Of course it is possible to configure some settings in order to tweak the default configuration for the flask extension:

.. code-block:: yaml

    ioc.extra.flask:
        port:               8080
        name:               ''
        static_path:        ''
        static_url_path:    ''
        static_folder:      'static'
        template_folder:    'templates'
        instance_path:      ''
        instance_relative_config: false

So an extension is a way of sharing services accross libraries and to avoid bootstraping code.

