from ioc.extra.command import Command
import tornado
from tornado.httpserver import HTTPServer

class StartCommand(Command):
    def __init__(self, application, router):
        self.application = application
        self.router = router

    def initialize(self, parser):
        parser.description = 'Start tornado integrated server'
        parser.add_argument('--address', '-a', default='0.0.0.0', help="the host to bind the port")
        parser.add_argument('--port', '-p', default=5000, type=int, help="the port to listen")
        parser.add_argument('--processes', '-np', default=1, type=int, help="number of processes to start (0=cores available)")
        parser.add_argument('--bind', '-b', default="localhost", type=str, help="bind the router to the provided named (default=localhost)")

    def execute(self, args, output):
        output.write("Starting tornado %s:%s\n" % (args.address, args.port))

        self.router.bind(args.bind)

        server = HTTPServer(self.application)
        server.bind(args.port, args.address)
        server.start(args.processes)

        output.write("Waiting for connection...\n")

        tornado.ioloop.IOLoop.instance().start()