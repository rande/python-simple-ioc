Tag
===

Service definition can be tagged in order to be found while the container is being build.

For instance, a jinja filters can be define like this::

    jinja.filter.time:
        class: jinja.extra.filter.Time
        tags:
            jinja.filter: # a filter can have multiple filter options
                - []  
                - []

Then, while the container is being build, it is possible to attach new service to the ``jinja`` instance

.. code-block:: python

    class Extension(ioc.component.Extension):
        def load(self, config, container_builder):

            # ...

            jinja = container_builder.get('jinja')

            for id in container_builder.get_ids_by_tags('jinja.filter'):
                definition = container_builder.get(id)

                for options in definition.get_tag('jinja.filter'):
                    jinja.add_call('register_filter', ioc.component.Reference(id))

