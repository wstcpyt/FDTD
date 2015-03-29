__author__ = 'yutongpang'
import unittest
from fdtdcode.source import Source
from unittest.mock import patch


class SourceTest(unittest.TestCase):
    def setUp(self):
        self.source = Source(1)

    @patch.object(Source, '_init_constant_variable')
    def test_init_source(self, mock_init_constant_variable):
        self.source = Source(1)
        mock_init_constant_variable.assert_called_once_with(1)

    def test_init_constant_variable(self):
        self.assertEqual(self.source.points_per_wavelength, 40)
        self.assertEqual(self.source.source_node_index, 1)

    def test_get_additive_source_function_at_time_node_index(self):
        result = self.source.get_additive_source_function_at_time_node_index(0, 0)
        self.assertEqual(result, 0)