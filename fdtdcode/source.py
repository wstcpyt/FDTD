__author__ = 'yutongpang'
from math import pi, sin
from fdtdcode.field import Meshnodefield


class Source():
    def __init__(self):
        self._init_constant_variable()

    def _init_constant_variable(self):
        self.points_per_wavelength = 40

    def get_additive_source_function_at_time_node_index(self, time_node_index, field_node_index):
        source_function_value = sin(
            2.0 * pi / self.points_per_wavelength * (Meshnodefield.courant_number * time_node_index - field_node_index))
        return source_function_value