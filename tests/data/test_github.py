import unittest

from arxivtimes_indicator.data.github import *


class TestGitHub(unittest.TestCase):

    def test_get_all_issues(self):
        issues = get_all_issues()
        self.assertIsInstance(issues, list)
        self.assertTrue(len(issues) > 0)

    def test_tally_by_user(self):
        issues = [{'user': {'login': 'hoge'}},
                  {'user': {'login': 'hoge'}},
                  {'user': {'login': 'fuga'}}]
        names, counts = tally_by_users(issues)
        self.assertEqual(names, ['hoge', 'fuga'])
        self.assertEqual(counts, [2, 1])

    def test_tally_by_label(self):
        issues = [{'labels': [{'name': 'NLP'},
                              {'name': 'RNN'},
                              {'name': 'CNN'}]},
                  {'labels': [{'name': 'NLP'},
                              {'name': 'RNN'}]},
                  {'labels': [{'name': 'Dialogue'}]}]
        names, counts = tally_by_labels(issues)
        self.assertEqual(len(names), 4)
        self.assertEqual(counts, [2, 2, 1, 1])

    def test_filter_issue_by_ym(self):
        issues = get_all_issues()
        filtered_issues = filter_issue_by_ym(issues)
        self.assertTrue(len(filtered_issues) <= len(issues))
