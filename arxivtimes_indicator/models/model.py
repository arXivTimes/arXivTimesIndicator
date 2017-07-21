import os
import sys
from collections import defaultdict, Counter
from datetime import datetime

import dateutil.parser
import dateutil.relativedelta
from peewee import *
from playhouse.shortcuts import model_to_dict

from arxivtimes_indicator.data_api import DataApi


db = SqliteDatabase(os.path.join(os.path.join(os.path.dirname(__file__), '../../'), 'database.db'))
if "unittest" in sys.modules:
    db = SqliteDatabase(os.path.join(os.path.join(os.path.dirname(__file__), '../../tests/'), 'test_db.db'))


def create_tables():
    if not Issue.table_exists():
        db.create_table(Issue)
    if not Label.table_exists():
        db.create_table(Label)


def drop_tables():
    if Issue.table_exists():
        Issue.drop_table()
    if Label.table_exists():
        Label.drop_table()


class BaseModel(Model):
    class Meta:
        database = db


class Issue(BaseModel):
    title = CharField()
    url = CharField(unique=True)
    user_id = CharField()
    avatar_url = CharField()
    score = IntegerField()
    created_at = DateTimeField()
    body = TextField()

    @classmethod
    def extract_headline(cls, body):
        headline_left = len('## 一言でいうと')
        headline_right = body.find('###')  # until next section
        if headline_right > 0:
            headline = body[headline_left:headline_right].strip()
        else:
            headline = body
        return headline


class Label(BaseModel):
    issue = ForeignKeyField(Issue, related_name='labels')
    name = CharField()


class IndicatorApi(DataApi):

    def issue_to_dict(self, issue):
        issue_dict = model_to_dict(issue, backrefs=True)
        headline = Issue.extract_headline(issue_dict["body"])
        issue_dict["headline"] = headline
        labels = [lb["name"] for lb in issue_dict["labels"]]
        issue_dict["genres"] = self.labels_to_genres(labels)
        return issue_dict

    def get_recent(self, user_id='', limit=-1):
        if user_id:
            q = Issue.select().where(Issue.user_id==user_id).order_by(Issue.created_at).limit(limit)
        else:
            q = Issue.select().order_by(Issue.created_at).limit(limit)
        return [self.issue_to_dict(iss) for iss in q]

    def get_popular(self, user_id='', limit=-1):
        if user_id:
            q = Issue.select().where(Issue.user_id == user_id).order_by(Issue.score).limit(limit)
        else:
            q = Issue.select().order_by(Issue.score).limit(limit)
        return [self.issue_to_dict(iss) for iss in q]

    def aggregate_per_month(self, user_id='', month=6, use_genre=True):
        now = datetime.now()
        start_time = now - dateutil.relativedelta.relativedelta(months=month)
        start_time_str = start_time.strftime('%Y-%m-01 00:00:00+00:00')
        if user_id:
            issues = Issue.select().where(Issue.user_id == user_id).where(Issue.created_at >= start_time_str)
        else:
            issues = Issue.select().where(Issue.created_at >= start_time_str)
        stat = defaultdict(Counter)
        for issue in issues:
            key = dateutil.parser.parse(issue.created_at).strftime('%Y/%m')
            issue_d = self.issue_to_dict(issue)
            kinds = issue_d["genres"] if use_genre else issue_d["labels"]
            for k in kinds:
                stat[key][k] += 1

        genres = list(set(self.LABEL_TO_GENRE.values()))
        labels = list(self.LABEL_TO_GENRE.keys())
        kinds = genres if use_genre else labels
        _year, _month = start_time.year, start_time.month
        yms = []
        for i in range(month):
            ym = "{}/{}".format(_year, str(_month).zfill(2))
            if ym not in stat:
                stat[ym] = {}
            for k in kinds:
                if k not in stat[ym]:
                    stat[ym][k] = 0  # fill missing

            stat[ym] = dict(stat[ym])
            _month = _month + 1  # timedelta doesn't support month!
            if _month > 12:
                _month = _month - 12
                _year = _year + 1

        return stat

    def aggregate_kinds(self, user_id='', month=6, use_genre=True):
        ym_stat = self.aggregate_per_month(user_id, month, use_genre)
        stat = Counter()
        for kind_count in ym_stat.values():
            stat += kind_count
        
        return dict(stat)

    def get_user_total_score(self, user_id):
        score = Issue.select(fn.SUM(Issue.score)).where(Issue.user_id == user_id).group_by(Issue.user_id).scalar()
        return score

    def get_user_post_count(self, user_id):
        count = Issue.select(Issue.title).where(Issue.user_id == user_id).count()
        return count
