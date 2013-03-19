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
