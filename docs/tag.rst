Tag
===

Service definition can be tagged in order to be found while the container is being build.

For instance, a jinja filters can be define like this::

    jinja2.filter.time:
        class: jinja2.extra.filter.Time
        tags:
            jinja2.filter: # a filter can have multiple filter options
                - []  
                - []

Then, while the container is being build, it is possible to attach new service to the ``jinja`` instance

.. code-block:: python

    class Extension(ioc.component.Extension):
        def load(self, config, container_builder):

            # ...

            jinja = container_builder.get('ioc.extra.jinja2')

            for id in container_builder.get_ids_by_tags('jinja2.filter'):
                definition = container_builder.get(id)

                for options in definition.get_tag('jinja2.filter'):
                    jinja.add_call('register_filter', ioc.component.Reference(id))

