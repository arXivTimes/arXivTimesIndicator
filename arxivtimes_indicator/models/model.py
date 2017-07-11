from peewee import *

db = SqliteDatabase('my_app.db')


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

    def extract_headline(self):
        headline_left = len('## 一言でいうと')
        headline_right = self.body.index('###')  # until next section
        headline = self.body[headline_left:headline_right].strip()

        return headline


class Label(BaseModel):
    issue = ForeignKeyField(Issue, related_name='labels')
    name = CharField()

    def __init__(self, name):  # Aggregate label names
        super(Label, self).__init__()
        self.name = name


def get_recent(user_id, limit):
    Issue.select().where(Issue.user_id==user_id).order_by(Issue.created_at)


def get_popular(user_id, limit):
    Issue.select().where(Issue.user_id==user_id).order_by(Issue.score)


def aggregate_per_month(self, user_id="", month=6, use_genre=True):
    """
    Get aggreagation of post count per year_month and genre or label
    Args:
        user_id: to filter the records by user_id
        month: to limit the aggrecation time range
        use_genre: use genre to aggregate (when False then use label)
    Returns:
        aggregation: post count aggregation by year/month, genre(or label).
        example {"2017/01": {"genre1": 1, "genre2": 3, ...}}
        (The size of each year/month aggregation should be equal.
        You have to compensate 0 if the specific genres don't exist in that year/month.)
    """

    from datetime import datetime
    import dateutil.relativedelta
    import dateutil.parser
    from collections import defaultdict, Counter
    now = datetime.now()
    start_time = now - dateutil.relativedelta(months=month)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S+00:00")
    issues = Issue.select().where(Issue.user_id == user_id).where(Issue.created_at >= start_time_str)
    counter = defaultdict(Counter)
    for issue in issues:
        key = dateutil.parser.parse(issue.created_at).strftime('%Y/%m')
        for label in issue.labels:
            counter[key][label] += 1
    return counter


def aggregate_kinds(user_id="", month=6, use_genre=True):
    """
    Get aggreagation of post count per genre or label
    Args:
        user_id: to filter the records by user_id
        month: to limit the aggrecation time range
        use_genre: use genre to aggregate (when False then use label)
    Returns:
        aggregation: post count aggregation by genre(or label).
        example {"genre1": 11, "genre2": 31, ...}
    """
    from collections import Counter
    counters = aggregate_per_month(user_id, month, use_genre)
    counter = Counter()
    for c in counters.values():
        counter += c
    return counter
