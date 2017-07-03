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
