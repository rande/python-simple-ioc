Python Simple Dependency Injection Container
============================================

This project is a simple port of the Symfony2 DependencyInjection lib available at https://github.com/symfony/DependencyInjection

Status: Work In Progress

Usage
-----

- Services Definition

```yaml

parameters:
    foo.bar: parameter 1

services:
    fake:
        class: tests.ioc.service.Fake
        arguments: 
            - argument 1
        kargs:
            param: here a parameter

    foo:
        class: tests.ioc.service.Foo
        arguments: ["@fake"]
        kargs: {}
```

- Python 

```python

import ioc

container = ioc.build(['service.yml'])

foo = container.get('foo')

```