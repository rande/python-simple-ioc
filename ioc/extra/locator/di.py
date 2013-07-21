import ioc.loader, ioc.component, ioc.exceptions
from ioc.component import Definition

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        extensions = container_builder.parameters.get('ioc.extensions')

        locator_map = {}

        for extension in extensions:
            locator_map[extension] = Definition('ioc.locator.ChoiceLocator', 
                arguments=[[
                    Definition('ioc.locator.FileSystemLocator', arguments=["%s/resources/%s" % (container_builder.parameters.get('project.root_folder'), extension)]),
                    Definition('ioc.locator.PackageLocator', arguments=[extension], kwargs={'package_path': 'resources'})
                ]]
            )

        container_builder.add('ioc.locator', Definition('ioc.locator.PrefixLocator', arguments=[locator_map], kwargs={'delimiter': ':'}))
