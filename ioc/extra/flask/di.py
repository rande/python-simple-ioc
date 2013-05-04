import ioc.loader, ioc.component, ioc.exceptions
import os, datetime

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
        container_builder.parameters.set('ioc.extra.flask.app.port', app.get('port', 8080))

        self.configure_app_config(config, container_builder)
        self.configure_blueprint(config, container_builder)


    def configure_app_config(self, config, container_builder):

        defaults = {
            'DEBUG':                         False,
            'TESTING':                       False,
            'PROPAGATE_EXCEPTIONS':          None,
            'PRESERVE_CONTEXT_ON_EXCEPTION': None,
            'SECRET_KEY':                    None,
            'PERMANENT_SESSION_LIFETIME':    datetime.timedelta(days=31),
            'USE_X_SENDFILE':                False,
            'LOGGER_NAME':                   None,
            'SERVER_NAME':                   None,
            'APPLICATION_ROOT':              None,
            'SESSION_COOKIE_NAME':           'session',
            'SESSION_COOKIE_DOMAIN':         None,
            'SESSION_COOKIE_PATH':           None,
            'SESSION_COOKIE_HTTPONLY':       True,
            'SESSION_COOKIE_SECURE':         False,
            'MAX_CONTENT_LENGTH':            None,
            'SEND_FILE_MAX_AGE_DEFAULT':     12 * 60 * 60, # 12 hours
            'TRAP_BAD_REQUEST_ERRORS':       False,
            'TRAP_HTTP_EXCEPTIONS':          False,
            'PREFERRED_URL_SCHEME':          'http',
            'JSON_AS_ASCII':                 True
        }

        c = config.get_dict('config', {})

        for name, value in defaults.iteritems():
            container_builder.parameters.set('ioc.extra.flask.app.%s' % name, c.get(name, value))

        for name, value in c.all().iteritems():
            container_builder.parameters.set('ioc.extra.flask.app.%s' % name, c.get(name, value))
            defaults[name] = value

        container_builder.parameters.set('ioc.extra.flask.app.instance_relative_config', defaults)


    def configure_blueprint(self, config, container_builder):

        definition = container_builder.get('ioc.extra.flask.app')

        for id, kwargs in config.get_dict('blueprints', {}).all().iteritems():
            definition.add_call('register_blueprint', [ioc.component.Reference(id)], kwargs.all())

    def post_build(self, container):
        if container.has('jinja.env'):
            raise ioc.exceptions.DuplicateServiceDefinition()

        container.set('jinja.env', container.get('ioc.extra.flask.app').jinja_env)
        container.set('jinja.loader', container.get('ioc.extra.flask.app').jinja_loader)


