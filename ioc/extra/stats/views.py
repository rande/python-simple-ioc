class IndexView(object):
    def __init__(self, container):
        self.container = container

    def execute(self, context):
        pass

class ParametersView(object):
    def __init__(self, container):
        self.container = container

    def execute(self, context, type=None):
        flask = context.settings['flask']
        
        context.node.title = "Parameters"

        params = {
            'parameters': self.container.parameters,
            'context': context
        }

        return flask.make_response(flask.render_template('ioc.extra.stats:parameters.html', **params))

class ServicesView(object):
    def __init__(self, container):
        self.container = container

    def execute(self, context):
        flask = context.settings['flask']

        context.node.title = "Services"

        params = {
            'services': self.container.services,
            'context': context,
        }

        return flask.make_response(flask.render_template('ioc.extra.stats:services.html', **params))
