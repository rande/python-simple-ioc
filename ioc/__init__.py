import ioc.component
import ioc.loader

def build(files):

    container_builder = ioc.component.ContainerBuilder()
    
    loaders = [
        ioc.loader.YamlLoader
    ]

    for file in files:
        for loader in loaders:
            if not loader.support(file):
                continue

            loader.load(open(file), container_builder)