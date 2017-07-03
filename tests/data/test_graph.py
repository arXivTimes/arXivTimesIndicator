import os
import unittest

from PIL import Image

from arxivtimes_indicator.visualization.visualize import *


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.x = [1, 2, 3]
        self.y = [3, 2, 1]
        self.file_name = 'test.png'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_save_graph(self):
        save_bar_graph(self.x, self.y, self.file_name)
        self.assertTrue(os.path.exists(self.file_name))

    def test_save_graph_with_icon(self):
        image_path = os.path.join(os.path.dirname(__file__), 'data', '128x128.png')
        image_paths = [image_path for _ in range(len(self.x))]
        images = [Image.open(p) for p in image_paths]
        save_graph_with_icon(self.x, self.y, images, self.file_name)
        self.assertTrue(os.path.exists(self.file_name))