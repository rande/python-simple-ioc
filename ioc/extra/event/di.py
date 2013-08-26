import ioc.loader, ioc.component, ioc.exceptions
import os, datetime

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        container_builder.add('ioc.extra.event_dispatcher', ioc.component.Definition('ioc.event.Dispatcher'))

    def post_build(self, container_builder, container):
        dispatcher = container.get('ioc.extra.event_dispatcher')

        for id in container_builder.get_ids_by_tag('event.listener'):
            definition = container_builder.get(id)
            for option in definition.get_tag('event.listener'):
                if 'name' not in option:
                    break

                if 'method' not in option:
                    break                

                if 'priority' not in option:
                    option['priority'] = 0

                dispatcher.add_listener(option['name'], getattr(container.get(id), option['method']), option['priority'])