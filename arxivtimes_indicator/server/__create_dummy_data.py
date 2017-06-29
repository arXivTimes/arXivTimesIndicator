import os
import re
import json
import numpy as np
import requests


def get_arxivtimes_issue():
    url = "https://api.github.com/repos/arXivTimes/arXivTimes/issues"
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
            "url": iss["url"],
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
