#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
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


class TornadoManager(object):
    STOPPED = 0
    STARTED = 1

    def __init__(self):
        self.ioloops = {}
        self.status = {}

    def add_ioloop(self, name, ioloop):
        self.ioloops[name] = ioloop
        self.status[name] = TornadoManager.STOPPED

    def stop(self, name):
        if self.status[name] == TornadoManager.STARTED:
            self.ioloops[name].stop()

    def start(self, name):
        if self.status[name] == TornadoManager.STOPPED:
            self.ioloops[name].start()

    def start_all(self):
        for name, loop in self.ioloops.iteritems():
            self.start(name)

    def stop_all(self):
        for name, loop in self.ioloops.iteritems():
            self.stop(name)
