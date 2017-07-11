import os
import re
import json
from datetime import datetime
import numpy as np
import requests
from arxivtimes_indicator.server.data_api import DataApi


class DummyData(DataApi):

    @classmethod
    def is_dummy_request(cls, request_handler):
        is_dummy = False
        is_dummy = request_handler.get_argument("dummy", "")
        if is_dummy and is_dummy.lower() == "true":
            is_dummy = True
        return is_dummy

    def get_recent(self, user_id="", limit=-1):
        path = os.path.join(os.path.dirname(__file__), "./_data/dummy_data.json")
        with open(path) as f:
            posts = json.load(f)
            for p in posts:
                p["genres"] = ["" if lb not in self.LABEL_TO_GENRE else self.LABEL_TO_GENRE[lb] for lb in p["labels"]]
                p["genres"] = [g for g in p["genres"] if g]

            if user_id:
                posts = [p for p in posts if p["user_id"] == user_id]
        return posts

    def get_popular(self, user_id="", limit=-1):
        ps = self.get_recent(user_id, limit)
        ps = sorted(ps, key=lambda p: p["score"], reverse=True)
        return ps

    def get_user_post_count(self, user_id):
        return 100

    def get_user_total_score(self, user_id):
        return 50

    def aggregate_per_month(self, user_id="", month=6, use_genre=True):
        posts = self.get_recent(user_id)
        stat = {}
        get_ym = lambda date_str: date_str.split("T")[0].rsplit("-", 1)[0].replace("-", "/")
        for p in posts:
            ym = get_ym(p["created_at"])
            kinds = p["genres"] if use_genre else p["labels"]

            if ym not in stat:
                stat[ym] = {}
            for k in kinds:
                if k not in stat[ym]:
                    stat[ym][k] = 0
                stat[ym][k] += 1
        
        genres = list(set(self.LABEL_TO_GENRE.values()))
        labels = list(self.LABEL_TO_GENRE.keys())
        kinds = genres if use_genre else labels
        _year, _month = datetime.now().year, datetime.now().month
        yms = []
        for i in range(month):
            yms.append("{}/{}".format(_year, str(_month).zfill(2)))
            _month = _month - 1
            if _month <= 0:
                _month = _month + 12
                _year = _year - 1
        for ym in yms:
            if ym not in stat:
                stat[ym] = {}
            for k in kinds:
                if k not in stat[ym]:
                    stat[ym][k] = 0  # fill missing

        return stat

    def aggregate_kinds(self, user_id="", month=6, use_genre=True):
        posts = self.get_recent(user_id)
        stat = {}
        for p in posts:
            kinds = p["genres"] if use_genre else p["labels"]

            for k in kinds:
                if k not in stat:
                    stat[k] = 0
                stat[k] += 1
        
        return stat

def get_arxivtimes_issue():
    url = "https://api.github.com/repos/arXivTimes/arXivTimes/issues?per_page=120"
    r = requests.get(url)
    issues = r.json()
    if not r.ok:
        r.raise_for_status()
    
    data = []
    scores = np.random.randint(100, size=len(issues))
    scores = [int(s) for s in scores]

    for i, iss in enumerate(issues):
        headline_left = len("## 一言でいうと")
        headline_right = iss["body"].index("###")  # until next section
        headline = iss["body"][headline_left:headline_right].strip()

        d = {
            "title": iss["title"],
            "url": iss["html_url"],
            "user_id": iss["user"]["login"],
            "avatar_url": iss["user"]["avatar_url"],
            "score": scores[i],
            "created_at": iss["created_at"],
            "labels": [lb["name"] for lb in iss["labels"]],
            "headline": headline
        }

        data.append(d)
    
    path = os.path.join(os.path.dirname(__file__), "./_data")
    if not os.path.exists(path):
        os.mkdir(path)

    d = json.dumps(data)
    with open(os.path.join(path, "dummy_data.json"), "wb") as f:
        f.write(d.encode("utf-8"))
    

"""
{
    "title": "Computer Vision Article",
    "url": "https://github.com/arXivTimes/arXivTimes/issues/343",
    "user_id": "github_user1",
    "avatar_url": "https://avatars3.githubusercontent.com/u/544269?v=3",
    "score": 60,
    "created_at": "2008-01-14T04:33:35Z",
    "labels": ["CNN", "Computer Vision"]
}
"""


if __name__ == "__main__":
    get_arxivtimes_issue()
