import os
import unittest

from arxivtimes_indicator.data.twitter import load_keys


class TestTwitterAPI(unittest.TestCase):

    def test_load_empty_keys(self):
        res = load_keys()
        self.assertEqual(res, tuple([None]*4))

    def test_load_keys(self):
        os.environ['CONSUMER_KEY'] = 'A'
        os.environ['CONSUMER_SECRET'] = 'B'
        os.environ['ACCESS_TOKEN'] = 'C'
        os.environ['ACCESS_TOKEN_SECRET'] = 'D'
        res = load_keys()
        self.assertEqual(res, ('A', 'B', 'C', 'D'))
