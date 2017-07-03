import unittest
from datetime import datetime

from arxivtimes_indicator.models.model import *


class TestCreateTable(unittest.TestCase):

    def test_create_table(self):
        self.assertFalse(Issue.table_exists())
        self.assertFalse(Label.table_exists())
        create_tables()
        self.assertTrue(Issue.table_exists())
        self.assertTrue(Label.table_exists())
        drop_tables()


class TestIssue(unittest.TestCase):

    def setUp(self):
        create_tables()

    def test_create(self):
        title = 'test_title'
        url = 'https://github.com/arXivTimes/arXivTimes/issues/350'
        user_id = 'icoxfog417'
        avatar_url = 'https://avatars2.githubusercontent.com/u/544269?v=3'
        score = 55
        created_at = datetime.now()
        body = 'test_body'
        labels = [Label(name='CV'), Label(name='NLP')]
        issue = Issue(title=title,
                      url=url,
                      user_id=user_id,
                      avatar_url=avatar_url,
                      score=score,
                      created_at=created_at,
                      body=body,
                      labels=labels)
        self.assertEqual(issue.title, title)
        self.assertEqual(issue.url, url)
        self.assertEqual(issue.user_id, user_id)
        self.assertEqual(issue.avatar_url, avatar_url)
        self.assertEqual(issue.score, score)
        self.assertEqual(issue.created_at, created_at)
        self.assertEqual(issue.body, body)
        self.assertEqual(issue.labels, labels)

    def test_count(self):
        self.assertEqual(len(Issue.select()), 0)
        issue = Issue(title='title', url='url', user_id='user_id', avatar_url='avatar_url',
                      score=50, created_at=datetime.now(), body='body', labels=[])
        issue.save()
        self.assertEqual(len(Issue.select()), 1)

    def test_extract_headline(self):
        body = """## 一言でいうと

        End-to-Endの対話システムを構築するためのデータセットが公開。50万発話でが含まれ、ドメインはレストラン検索となっている。発話に対しては固有表現(slot)的なアノテーションもされている(「フレンチが食べたい。500円くらいで」なら、種別=フレンチ、予算=500円など)。

        ### 論文リンク

        https://arxiv.org/abs/1706.09254"""
        issue = Issue(title='title', url='url', user_id='user_id', avatar_url='avatar_url',
                      score=50, created_at=datetime.now(), body=body, labels=[])
        headline = issue.extract_headline()
        result = '''End-to-Endの対話システムを構築するためのデータセットが公開。50万発話でが含まれ、ドメインはレストラン検索となっている。発話に対しては固有表現(slot)的なアノテーションもされている(「フレンチが食べたい。500円くらいで」なら、種別=フレンチ、予算=500円など)。'''
        self.assertEqual(headline, result)

    def tearDown(self):
        drop_tables()
