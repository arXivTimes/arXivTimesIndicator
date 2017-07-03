import os
import json
import tornado.web
import pandas as pd


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        is_dummy = self.get_argument("dummy", "")
        if is_dummy and is_dummy.lower() == "true":
            is_dummy = True
        
        papers = {}
        if is_dummy:
            path = os.path.join(os.path.dirname(__file__), "./_data/dummy_data.json")
            with open(path) as f:
                issues = json.load(f)
            papers = {
                "recent": issues,
                "popular": sorted(issues, key=lambda p: p["score"], reverse=True)
            }
            papers = json.dumps(papers)
        else:
            # todo: extract data from url
            pass
        
        self.render("index.html", papers=papers)


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
