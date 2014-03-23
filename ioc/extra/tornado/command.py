from ioc.extra.command import Command
import tornado
from tornado.httpserver import HTTPServer


class StartCommand(Command):

    def __init__(self, application):
        self.application = application

    def initialize(self, parser):
        parser.description = 'Start tornado integrated server'
        parser.add_argument('--address', '-a', default='0.0.0.0', help="the host to bind the port")
        parser.add_argument('--port', '-p', default=5000, type=int, help="the port to listen")
        parser.add_argument('--processes', '-np', default=1, type=int, help="number of processes to start (0=cores available)")

    def execute(self, args, output):
        output.write("Starting tornado %s:%s\n" % (args.address, args.port))

        server = HTTPServer(self.application)
        server.bind(args.port, args.address)

        output.write("Waiting for connection...\n")
        server.start(args.processes)

        tornado.ioloop.IOLoop.instance().start()