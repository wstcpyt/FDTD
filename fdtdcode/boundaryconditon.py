__author__ = 'yutongpang'
from math import exp
from fdtdcode.field import Singlenodefield


class TFSFboundarycondition():
    def __init__(self, magnetic_tfsf_node_index):
        self.magnetic_tfsf_node_index = magnetic_tfsf_node_index

    def get_incidence_source_correction(self, time_node_index, node_correction):
        if node_correction == 0:
            correction = self.__get_magnetic_source_correction(time_node_index)
        else:
            correction = self.__get_electric_source_correction(time_node_index)
        return correction

    @staticmethod
    def __get_magnetic_source_correction(time_node_index):
        return exp(-(time_node_index - 30.0)**2/100.0)/Singlenodefield.updatecoefficient

    @staticmethod
    def __get_electric_source_correction(time_node_index):
        return exp(-(time_node_index - 30.0 + 1)**2/100.0)