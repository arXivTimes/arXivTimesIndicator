import os
import json
import tornado.web
import requests
from arxivtimes_indicator.models.model import IndicatorApi
from arxivtimes_indicator.server.__dummy_data import DummyData


DEFAULT_LIMIT = 100


class BaseHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        err_detail = ""
        if self.settings["debug"] and "exc_info" in kwargs:
            import traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            err_detail = "".join(lines)

        self.render("error.html", status_code=status_code, err_detail=err_detail)


class IndexHandler(BaseHandler):

    def get(self):
        posts = {}
        stat = {}
        api = IndicatorApi() if not DummyData.is_dummy_request(self) else DummyData()
        recent = api.get_recent(limit=DEFAULT_LIMIT)
        quality = api.get_qualified(limit=DEFAULT_LIMIT)
        stat = api.aggregate_per_month()
        posts = {
            "recent": recent,
            "quality": quality
        }
        posts = json.dumps(posts)
        stat = json.dumps(stat)

        self.render("index.html", posts=posts, stat=stat)


class UserHandler(BaseHandler):

    def get(self, user_id):
        profile = {
            "user_id": user_id,
            "avatar_url": self.static_url("images/GitHub-Mark-64px.png"),
            "url": "",
            "name": user_id,
            "belongs": "",
            "blog": "",
            "total_score": 0,
            "post_count": 0
        }

        url = "https://api.github.com/users/{}".format(user_id)
        not_yet = False
        try:
            r = requests.get(url)
            if r.ok:
                p = r.json()
                profile["avatar_url"] = p["avatar_url"]
                profile["url"] = p["html_url"]
                profile["name"] = p["name"]
                if p["company"] or p["location"]:
                    if p["company"] and p["location"]:
                        profile["belongs"] = "at " + p["company"] + "," + p["location"]
                    elif p["company"]:
                        profile["belongs"] = "at " + p["company"]
                    elif p["location"]:
                        profile["belongs"] = "in " + p["location"]

                profile["blog"] = p["blog"]
                profile["location"] = p["location"]
            else:
                r.raise_for_status()

        except requests.exceptions.HTTPError as hex:
            not_yet = True
        except Exception as ex:
            print(ex)
        
        posts = {"recent":[], "quality":[]}
        stats = {"monthly":{}, "kinds": {}}

        api = IndicatorApi() if not DummyData.is_dummy_request(self) else DummyData()

        recent = api.get_recent(user_id=user_id, limit=DEFAULT_LIMIT)
        if not recent or len(recent) == 0:
            not_yet = True
        
        if not_yet:
            self.render("not_yet.html", user_id=user_id)

        posts["recent"] = recent
        profile["total_score"] = api.get_user_total_score(user_id)
        profile["post_count"] = api.get_user_post_count(user_id)
        quality = api.get_qualified(user_id=user_id, limit=DEFAULT_LIMIT)
        posts["quality"] = quality

        monthly = api.aggregate_per_month(user_id)
        kinds = api.aggregate_kinds(user_id)
        stats["monthly"] = monthly
        stats["kinds"] = kinds
        stats = json.dumps(stats)

        self.render("user.html", profile=profile, posts=posts, stats=stats)


class StatisticsHandler(tornado.web.RequestHandler):

    def get(self, user_id): 
        self.render("statistics.html")



class App404Handler(tornado.web.RequestHandler):

    def prepare(self):
        self.set_status(404)
        self.render("404.html")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/user/([^/]+)", UserHandler),
            (r"/statistics", StatisticsHandler),
        ]

        debug = (os.getenv("DEBUG", "DEBUG") == "DEBUG")

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            default_handler_class=App404Handler,
            xsrf_cookies=True,
            debug=debug,
        )

        super(Application, self).__init__(handlers, **settings)
