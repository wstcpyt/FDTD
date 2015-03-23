__author__ = 'yutongpang'


class Source():
    def __init__(self, source_node_index):
        self.source_node = source_node_index

    @staticmethod
    def get_additive_source_function_at_time_node_index(time_node_index):
        source_function = 0*time_node_index
        return source_function