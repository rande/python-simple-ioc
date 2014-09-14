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

from werkzeug.routing import NotFound, RequestRedirect

import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.ioloop import IOLoop
from tornado.concurrent import Future

from ioc.extra.tornado.router import TornadoMultiDict

import mimetypes

class BaseHandler(tornado.web.RequestHandler):
    def dispatch(self):
        pass

    def get(self):
        return self.dispatch()

    def post(self):
        return self.dispatch()

    def put(self):
        return self.dispatch()

    def delete(self):
        return self.dispatch()

    def head(self):
        return self.dispatch()

    def options(self):
        return self.dispatch()

    def is_finish(self):
        return self._finished

    def get_header(self, name):
        return self._headers.get(name)

    def get_form_data(self):
        return TornadoMultiDict(self)

    def get_chunk_buffer(self):
        return b"".join(self._write_buffer)

    def has_header(self, name):
        return name in self._headers

    def is_xml_http_request(self):
        return 'X-Requested-With' in self.request.headers and 'XMLHttpRequest' == self.request.headers['X-Requested-With']

    def reset_chunk_buffer(self):
        self._write_buffer = []

class RouterHandler(BaseHandler):
    def initialize(self, router, event_dispatcher, logger=None):
        self.router = router
        self.event_dispatcher = event_dispatcher
        self.logger = logger

    @tornado.web.asynchronous
    def dispatch(self):
        result = None
        # the handler.request event might close the connection
        if self.is_finish():
            return

        try:
            name, parameters, callback = self.router.match(path_info=self.request.path, method=self.request.method)

            if self.logger:
                self.logger.debug("[ioc.extra.tornado.RouterHandler] Match name:%s with parameters:%s (%s)" % (name, parameters, callback))

            event = self.event_dispatcher.dispatch('handler.callback', {
                'request_handler': self,
                'request': self.request,
                'name': name,
                'callback': callback,
                'parameters': parameters
            })

            if self.is_finish():
                return

            result = event.get('callback')(self, **event.get('parameters'))

            if self.is_finish():
                return

        except RequestRedirect, e:
            if self.logger:
                self.logger.debug("%s: redirect: %s" % (__name__, e.new_url))

            self.redirect(e.new_url, True, 301)
            return

        except NotFound, e:
            if self.logger:
                self.logger.critical("%s: NotFound: %s" % (__name__, self.request.uri))

            self.set_status(404)

            self.event_dispatcher.dispatch('handler.not_found', {
                'request_handler': self,
                'request': self.request,
                'exception': e,
            })
        except Exception, e:
            self.set_status(500)

            import traceback

            if self.logger:
                self.logger.critical(traceback.print_exc())

            self.event_dispatcher.dispatch('handler.exception', {
                'request_handler': self,
                'request': self.request,
                'exception': e,
            })

        # the dispatch is flagged as asynchronous by default so we make sure the finish method will be called
        # unless the result of the callback is a Future
        if isinstance(result, Future):
            IOLoop.current().add_future(result, self.finish)
            return

        if not self.is_finish():
            self.finish(result=result)

    def prepare(self):
        if self.logger:
            self.logger.debug("[ioc.extra.tornado.RouterHandler] prepare request %s" % self.request.uri)

        self.event_dispatcher.dispatch('handler.request', {
            'request_handler': self,
            'request': self.request
        })

    def finish(self, *args, **kwargs):
        result = None
        if 'result' in kwargs:
            result = kwargs['result']

        if self.logger:
            self.logger.debug("[ioc.extra.tornado.RouterHandler] finish request %s" % self.request.uri)

        self.event_dispatcher.dispatch('handler.response', {
            'request_handler': self,
            'request': self.request,
            'result': result
        })

        super(RouterHandler, self).finish()

        if self.logger:
            self.logger.debug("[ioc.extra.tornado.RouterHandler] terminate request %s" % self.request.uri)

        self.event_dispatcher.dispatch('handler.terminate', {
            'request_handler': self,
            'request': self.request,
        })

    def send_file_header(self, file):
        mime_type, encoding = mimetypes.guess_type(file)

        if mime_type:
            self.set_header('Content-Type', mime_type)

    def send_file(self, file):
        """
        Send a file to the client, it is a convenient method to avoid duplicated code
        """
        if self.logger:
            self.logger.debug("[ioc.extra.tornado.RouterHandler] send file %s" % file)

        self.send_file_header(file)

        fp = open(file, 'rb')
        self.write(fp.read())

        fp.close()
