__author__ = 'yutongpang'
from math import exp


class Source():
    def __init__(self, source_node):
        self.source_node = source_node

    def get_additive_source_function_at_time_node_index(self, time_node_index):
        source_function = exp(-(time_node_index - 30.0)*(time_node_index - 30.0)/100)
        return source_function