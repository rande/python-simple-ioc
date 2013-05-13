import ioc.loader, ioc.component
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/command.yml" % path, container_builder)

    def post_build(self, container_builder, container):
        command_manager = container.get('ioc.extra.command.manager')

        for id in container_builder.get_ids_by_tag('command'):
            definition = container_builder.get(id)
            for option in definition.get_tag('command'):
                if 'name' not in option:
                    break

                command_manager.add_command(option['name'], container.get(id))

