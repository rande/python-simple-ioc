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

import argparse

class Command(object):

    def initialize(self, parser):
        pass

    def execute(self, args, output):
        pass

class CommandManager(object):
    def __init__(self, commands=None):
        self.commands = commands or {}

    def add_command(self, name, command):
        parser = argparse.ArgumentParser(prog=name) 

        # default share arguments
        parser.add_argument('--verbose', '-v', action='count', help="verbose level")
        parser.add_argument('--debug', '-d', help="debug mode", action='store_true')
        parser.add_argument('--env', '-e', help="Define the environement")

        command.initialize(parser)

        self.commands[name] = (parser, command)

    def execute(self, argv, stdout):
        argv.pop(0)  # remove the script name

        if len(argv) == 0:  # no argument
            name = 'help'
            argv = []
        else:
            name = argv.pop(0)

        if name not in self.commands:
            name = 'help'

        parser, command = self.commands[name]

        arguments = parser.parse_args(argv)

        r = command.execute(arguments, stdout)

        if r is None:
            r = 0

        return r

class HelpCommand(Command):

    def __init__(self, command_manager):
        self.command_manager = command_manager

    def initialize(self, parser):
        parser.description = 'Display available commands'
        pass

    def execute(self, args, output):
        output.write("Commands available: \n")
        for name, (parser, command) in self.command_manager.commands.items():
            output.write(" > % -20s : %s \n" % (name, parser.description))

        output.write("\n--\nPython IoC - Thomas Rabaix <thomas.rabaix@gmail.com>\n")
