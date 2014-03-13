from werkzeug.routing import NotFound

import tornado.web
import tornado.httpclient

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

class RouterHandler(BaseHandler):
    def initialize(self, router, event_dispatcher):
        self.router = router
        self.event_dispatcher = event_dispatcher

    def dispatch(self):
        try:
            self.event_dispatcher.dispatch('handler.request', {'handler': self})

            name, parameters, callback = self.router.match(path_info=self.request.path, method=self.request.method)

            event = self.event_dispatcher.dispatch('handler.callback', {
                'handler': self,
                'name': name,
                'callback': callback,
                'parameters': parameters
            })

            event.get('callback')(self, **event.get('parameters'))

        except NotFound:
            self.set_status(404)
            self.write("Not Found")

            self.event_dispatcher.dispatch('handler.not_found', {
                'handler': self,
            })
        except Exception:
            self.set_status(500)
            self.write("An unexpected error occurred")

            self.event_dispatcher.dispatch('handler.exception', {
                'handler': self,
            })

        self.event_dispatcher.dispatch('handler.response', {
            'handler': self,
        })

        self.finish()

        self.event_dispatcher.dispatch('handler.terminate', {
            'handler': self,
        })
