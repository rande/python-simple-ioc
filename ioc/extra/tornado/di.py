import ioc
import os
from ioc.extra.tornado.handler import RouterHandler
from tornado.web import StaticFileHandler

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/services.yml" % path, container_builder)

        container_builder.parameters.set('ioc.extra.tornado.static_folder',      config.get('static_folder', '%project.root_folder%/resources/static'))
        container_builder.parameters.set('ioc.extra.tornado.static_public_path', config.get('static_public_path', '/static'))

    def post_load(self, container_builder):
        if not container_builder.has('ioc.extra.jinja2'):
            return

        definition = container_builder.get('ioc.extra.tornado.router')
        definition.add_tag('jinja2.global', {'name': 'url_for', 'method': 'generate'})

        definition = container_builder.get('ioc.extra.tornado.asset_helper')
        definition.add_tag('jinja2.global', {'name': 'asset', 'method': 'generate_asset'})

    def post_build(self, container_builder, container):
        self.container = container

        container.get('ioc.extra.event_dispatcher').add_listener('ioc.extra.tornado.start', self.configure_tornado)

    def configure_tornado(self, event):

        application = event.get('application')

        self.container.get('logger').info("Attach ioc.extra.tornado.router.RouterHandler")

        application.add_handlers(".*$", [
            ("/.*", RouterHandler, {
                "router":           self.container.get('ioc.extra.tornado.router'),
                "event_dispatcher": self.container.get('ioc.extra.event_dispatcher'),
                "logger":           self.container.get('logger')
            })
        ])

        self.container.get('logger').info("Attach tornado.web.StaticFileHandler")

        application.add_handlers(".*$", [
            (self.container.parameters.get("ioc.extra.tornado.static_public_path") + "/(.*)", StaticFileHandler, {
                "path": self.container.parameters.get("ioc.extra.tornado.static_folder")
            })
        ])
