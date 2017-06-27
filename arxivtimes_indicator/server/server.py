import os
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="title")


class UserHandler(tornado.web.RequestHandler):

    def get(self, user_id):
        self.render("user.html", user_id=user_id)


class StatisticsHandler(tornado.web.RequestHandler):

    def get(self, user_id):
        self.render("statistics.html")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/user/([^/]+)", UserHandler),
            (r"/statistics", StatisticsHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            xsrf_cookies=True,
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)
