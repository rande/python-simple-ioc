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

class Manager(object):
    def __init__(self, default=None, connections=None, clients=None):
        self.connections = connections or {}
        self.clients = clients or {}
        self.default = default or False

    def add_connection(self, name, connection):
        self.connections[name] = connection

    def get_connection(self, name=None):
        if len(self.connections) == 1:
            return self.connections.values()[0]

        if name in self.connections:
            return self.connections[name]

        raise KeyError('Unable to find the the valid connection')

    def add_client(self, name, client):
        self.clients[name] = client

    def get_default_client(self):
        if len(self.clients) == 1:
            return self.clients.values()[0]

        if not self.default:
            raise KeyError('No default client set')

        return self.get_client(self, name=self.default)
        
    def get_client(self, name=None):
        if not name:
            return self.get_default_client()

        if name in self.clients:
            return self.clients[name]

        raise KeyError('Unable to find the the valid connection')
