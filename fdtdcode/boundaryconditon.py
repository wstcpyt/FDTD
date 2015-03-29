__author__ = 'yutongpang'
from math import exp
from fdtdcode.field import Meshnodefield
from fdtdcode.source import Source


class TFSFboundarycondition():
    def __init__(self, magnetic_tfsf_node_index):
        self.source = Source()
        self.magnetic_tfsf_node_index = magnetic_tfsf_node_index

    def get_incidence_source_correction(self, time_node_index, node_correction):
        if node_correction == 0:
            correction = self._get_magnetic_source_correction(time_node_index)
        else:
            correction = self._get_electric_source_correction(time_node_index)
        return correction

    def _get_magnetic_source_correction(self, time_node_index):
        return self.source.get_additive_source_function_at_time_node_index(time_node_index,
                                                                           0) / Meshnodefield.updatecoefficient

    def _get_electric_source_correction(self, time_node_index):
        return self.source.get_additive_source_function_at_time_node_index(time_node_index + 0.5, -0.5)