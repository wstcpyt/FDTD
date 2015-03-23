__author__ = 'yutongpang'
import unittest
from fdtdcode.source import Source


class SourceTest(unittest.TestCase):
    def setUp(self):
        self.source = Source(1)

    def test_source_can_init_source_node(self):
        pass

    def test_set_additive_source_time_dependent_functon(self):
        self.source.get_additive_source_function_at_time_node_index(20)