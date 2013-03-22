import ioc.loader, ioc.component
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/flask.yml" % path, container_builder)

        container_builder.parameters.set('ioc.extra.flask.app.name', config.get('name', ''))
        container_builder.parameters.set('ioc.extra.flask.app.static_path', config.get('static_path', ''))
        container_builder.parameters.set('ioc.extra.flask.app.static_url_path', config.get('static_url_path', 'static'))
        container_builder.parameters.set('ioc.extra.flask.app.instance_path', config.get('instance_path', 'templates'))
        container_builder.parameters.set('ioc.extra.flask.app.template_folder', config.get('template_folder', ''))
        container_builder.parameters.set('ioc.extra.flask.app.instance_relative_config', config.get('instance_relative_config', False))
        container_builder.parameters.set('ioc.extra.flask.app.port', config.get('port', 8080))
