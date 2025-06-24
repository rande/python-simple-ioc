#
# Copyright 2014-2025 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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

        # flask autoreload cannot read from arguments line
        if args.debug:
            options['debug'] = True
            options['use_reloader'] = False
            options['use_debugger'] = False

        self.flask.run(**options)
