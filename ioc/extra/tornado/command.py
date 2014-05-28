from ioc.extra.command import Command
import tornado
from tornado.httpserver import HTTPServer

class StartCommand(Command):
    def __init__(self, application, router, event_dispatcher):
        self.application = application
        self.event_dispatcher = event_dispatcher
        self.router = router

    def initialize(self, parser):
        parser.description = 'Start tornado integrated server'
        parser.add_argument('--address', '-a', default='0.0.0.0', help="the host to bind the port")
        parser.add_argument('--port', '-p', default=5000, type=int, help="the port to listen")
        parser.add_argument('--processes', '-np', default=1, type=int, help="number of processes to start (0=cores available)")
        parser.add_argument('--bind', '-b', default="localhost", type=str, help="bind the router to the provided named (default=localhost)")

    def execute(self, args, output):

        output.write("Configuring tornado (event: ioc.extra.tornado.start)\n")

        self.event_dispatcher.dispatch('ioc.extra.tornado.start', {
            'application': self.application,
            'output': output
        })

        output.write("Starting tornado %s:%s (bind to: %s)\n" % (args.address, args.port, args.bind))

        self.router.bind(args.bind)

        server = HTTPServer(self.application)
        server.bind(args.port, args.address)
        server.start(args.processes)

        output.write("Waiting for connection...\n")

        tornado.ioloop.IOLoop.instance().start()