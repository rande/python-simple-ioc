from element.node import NodeHandler

class IndexView(object):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context):

        return 200, 'ioc.extra.stats:index.html', {}

class ParametersView(NodeHandler):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context, type=None):

        params = {
            'parameters': self.container.parameters,
            'context': context
        }

        return self.render(request_handler, self.container.get('ioc.extra.jinja2'), 'ioc.extra.stats:parameters.html', params)

class ServicesView(NodeHandler):
    def __init__(self, container):
        self.container = container

    def execute(self, request_handler, context):
        context.node.title = "Services"

        return 200, 'ioc.extra.stats:services.html', {
            'services': self.container.services,
            'context': context,
        }
