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

class RouterHandler(BaseHandler):
    def initialize(self, router, event_dispatcher, logger=None):
        self.router = router
        self.event_dispatcher = event_dispatcher
        self.logger = logger

    @tornado.web.asynchronous
    def dispatch(self):

        result = None
        # the handler.request might close the connection
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
            self.finish()

    def prepare(self):
        self.event_dispatcher.dispatch('handler.request', {
            'request_handler': self,
            'request': self.request
        })

    def finish(self, *args, **kwargs):
        self.event_dispatcher.dispatch('handler.response', {
            'request_handler': self,
            'request': self.request,
        })

        super(RouterHandler, self).finish()

        self.event_dispatcher.dispatch('handler.terminate', {
            'request_handler': self,
            'request': self.request,
        })

    def send_file(self, file):
        """
        Send a file to the client, it is a convenient method to avoid duplicated code
        """
        mime_type, encoding = mimetypes.guess_type(file)

        if mime_type:
            self.set_header('Content-Type', mime_type)

        fp = open(file, 'rb')
        self.write(fp.read())

        fp.close()
