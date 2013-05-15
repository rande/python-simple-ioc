from ioc.extra.command import Command

class StartCommand(Command):

    def __init__(self, flask):
        self.flask = flask

    def initialize(self, parser):
        parser.description = 'Start flask integrated server'
        parser.add_argument('--host', default='0.0.0.0', help="the host to bind the port")
        parser.add_argument('--port', default=5000, type=int, help="the port to listen")

    def execute(self, args, output):
        output.write("Starting flask...\n")

        options = {
            'host': args.host,
            'port': args.port,
        }

        ## flask autoreload cannot read from arguments line
        if args.debug:
            options['debug'] = True
            options['use_reloader'] = False
            options['use_debugger'] = False

        self.flask.run(**options)