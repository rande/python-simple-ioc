Extension
=========

An extension is a class used to configure services. A vendor might want to expose a configuration file to automatically generated valid services.

Here a flask extension, ``ioc.extra.flask.di.Extension``

.. code-block:: python

    import ioc.loader, ioc.component
    import os

    class Extension(ioc.component.Extension):
        def load(self, config, container_builder):

            path = os.path.dirname(os.path.abspath(__file__))

            # load an external file defining services
            loader = ioc.loader.YamlLoader()
            loader.load("%s/resources/config/flask.yml" % path, container_builder)

            # set default parameters into the container to be reuse by the container builder
            # or by external services
            container_builder.parameters.set('ioc.extra.flask.app.name', config.get('name', ''))
            container_builder.parameters.set('ioc.extra.flask.app.static_path', config.get('static_path', ''))
            container_builder.parameters.set('ioc.extra.flask.app.static_url_path', config.get('static_url_path', 'static'))
            container_builder.parameters.set('ioc.extra.flask.app.instance_path', config.get('instance_path', 'templates'))
            container_builder.parameters.set('ioc.extra.flask.app.template_folder', config.get('template_folder', ''))
            container_builder.parameters.set('ioc.extra.flask.app.instance_relative_config', config.get('instance_relative_config', False))
            container_builder.parameters.set('ioc.extra.flask.app.port', config.get('port', 8080))

How to use an extensions
------------------------

An extension is declared in the top yaml file by using its module name (``di.Extension`` is added by the ``ioc``), so in order to generate a flask instance just do:

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

and to use it:


.. code-block:: python


    import ioc

    container = ioc.build(['config.yml'])

    app = container.get('ioc.extra.flask.app')

    __name__ == ’__main__’:
        app.run()

Going further
-------------

The previous example is a bit overkill as Flask itself required a minimun amount of code to run. However the previous code allows to configure the default port which can be usefull for running different configurations.

Now, the ``ioc.extra.flask.app`` is available inside the container, so other services can use it.

The ``shirka`` project exposes some ``flask`` actions as service:

.. code-block:: yaml

    shirka.flask.view.shirka_proc_list:
        class: [shirka.control.proc, ProcListView.as_view]
        arguments: 
            - shirka_proc_list
            - "%shirka.data.dir%/proc"

    shirka.flask.view.shirka_proc_view:
        class: [shirka.control.proc, ProcView.as_view]
        arguments: 
            - shirka_proc_view
            - "%shirka.data.dir%/proc"

So there are 2 actions as a service defined here : ``shirka.flask.view.shirka_proc_view`` and ``shirka.flask.view.shirka_proc_list``. As you can note, we are injected custom parameters into each service, these parameters can be configured by the user in an external file.

The ``shirka`` project also provide a custom extension ``shirka.di.Extension``, this extension will register theses services as methods call to the ``ioc.extra.flask`` service.

.. code-block:: python

    import ioc
    import os

    class Extension(ioc.component.Extension):

        def pre_build(self, container_builder, container):

            # if the service does not exist, then avoid registering services
            if not container_builder.has('ioc.extra.flask.app'):
                return

            definition = container_builder.get('ioc.extra.flask.app')

            base_url = container_builder.parameters.get('shirka.web.api.base_url')
            definition.method_calls.append([
                'add_url_rule', 
                ['%s/process' % base_url],
                {'view_func': ioc.component.Reference('shirka.flask.view.shirka_proc_list')}
            ])

            definition.method_calls.append([
                'add_url_rule', 
                ['%s/process/<id>' % base_url],       
                {'view_func': ioc.component.Reference('shirka.flask.view.shirka_proc_view')}
            ])

The ``pre_build`` method is called after all extensions are loaded, this allow extensions to alter service definitions.

shirka configuration defined inside the ``config.yml`` file::

    shirka:
        # public_dir:
        api:
            base_url: '/shirka/api'
        data_dir: '%base_dir%/data'

So through some configuration, the user can configure how the Flask action will be expose ``/shirka/api``.