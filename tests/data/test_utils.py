import os
import unittest

from arxivtimes_indicator.data.utils import download


class TestDownloader(unittest.TestCase):

    def test_valid_url(self):
        url = "https://avatars3.githubusercontent.com/u/544269?v=3"
        file_name = 'test.png'
        download(url, file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)

    def test_invalid_url(self):
        url = 'https://hogehogefugafuga1209u123'
        file_name = 'test.png'
        self.assertRaises(OSError, download, url, file_name)
