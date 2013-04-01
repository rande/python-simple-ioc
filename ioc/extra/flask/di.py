import ioc.loader, ioc.component
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/flask.yml" % path, container_builder)

        app = config.get_dict('app', {})

        container_builder.parameters.set('ioc.extra.flask.app.name', app.get('name', ''))
        container_builder.parameters.set('ioc.extra.flask.app.static_path', app.get('static_path', ''))
        container_builder.parameters.set('ioc.extra.flask.app.static_url_path', app.get('static_url_path', 'static'))
        container_builder.parameters.set('ioc.extra.flask.app.instance_path', app.get('instance_path', 'templates'))
        container_builder.parameters.set('ioc.extra.flask.app.template_folder', app.get('template_folder', ''))
        container_builder.parameters.set('ioc.extra.flask.app.instance_relative_config', app.get('instance_relative_config', False))
        container_builder.parameters.set('ioc.extra.flask.app.port', app.get('port', 8080))
