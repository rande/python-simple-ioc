import ioc.loader, ioc.component, ioc.exceptions
import os, datetime

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/flask.yml" % path, container_builder)

        app = config.get_dict('app', {})

        container_builder.parameters.set('ioc.extra.flask.app.name', app.get('name', ''))
        
        container_builder.parameters.set('ioc.extra.flask.app.static_folder', app.get('static_folder', 'static'))
        container_builder.parameters.set('ioc.extra.flask.app.static_path', app.get('static_path', ''))
        container_builder.parameters.set('ioc.extra.flask.app.static_url_path', app.get('static_url_path', 'static'))
        container_builder.parameters.set('ioc.extra.flask.app.instance_path', app.get('instance_path', 'templates'))
        container_builder.parameters.set('ioc.extra.flask.app.template_folder', app.get('template_folder', ''))
        container_builder.parameters.set('ioc.extra.flask.app.port', app.get('port', 8080))
        container_builder.parameters.set('ioc.extra.flask.app.instance_relative_config', app.get('instance_relative_config', False))

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
            'JSON_AS_ASCII':                 True,
            'JSON_SORT_KEYS':                True,
            'JSONIFY_PRETTYPRINT_REGULAR':   True,
        }

        c = config.get_dict('config', {})

        for name, value in defaults.iteritems():
            container_builder.parameters.set('ioc.extra.flask.app.%s' % name, c.get(name, value))

        for name, value in c.all().iteritems():
            container_builder.parameters.set('ioc.extra.flask.app.%s' % name, c.get(name, value))
            defaults[name] = value

        container_builder.parameters.set('ioc.extra.flask.app.config', defaults)

    def configure_blueprint(self, config, container_builder):
        definition = container_builder.get('ioc.extra.flask.app')

        for id, kwargs in config.get_dict('blueprints', {}).all().iteritems():
            definition.add_call('register_blueprint', [ioc.component.Reference(id)], kwargs.all())

    def post_build(self, container_builder, container):
        """
        This method make sure the flask configuration is fine, and 
        check the if ioc.extra.jinja2 service is available. If so, the 
        flask instance will use this service, by keeping the flask template 
        loader and the one registered at the jinja2
        """
        app = container.get('ioc.extra.flask.app')

        app.config.update(container_builder.parameters.get('ioc.extra.flask.app.config'))

        if container.has('ioc.extra.jinja2'):
            # This must be an instance of jinja.ChoiceLoader
            # This code replace the flask specific jinja configuration to use
            # the one provided by the ioc.extra.jinja2 code
            jinja2 = container.get('ioc.extra.jinja2')

            jinja2.loader.loaders.append(app.create_global_jinja_loader())

            for name, value in app.jinja_env.globals.iteritems():
                if name not in jinja2.globals:
                    jinja2.globals[name] = value                

            for name, value in app.jinja_env.filters.iteritems():
                if name not in jinja2.filters:
                    jinja2.filters[name] = value                

            app.jinja_env = jinja2