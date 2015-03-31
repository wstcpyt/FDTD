__author__ = 'yutongpang'
from fdtdcode.field import Meshnodefield
from fdtdcode.source import Source
from math import sqrt
import numpy as np


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


class Absorption():
    def __init__(self, mesh_size):
        self._init_constant_and_variable(mesh_size)
        self._set_absorption_leftend_coefficient()
        self._set_absorption_rightend_coefficient()

    def _init_constant_and_variable(self, mesh_size):
        self.mesh_size = mesh_size
        self.electric_field_update_coefficients_h = np.zeros(mesh_size)
        self.magnetic_field_update_coefficients_e = np.zeros(mesh_size)

    def _set_absorption_leftend_coefficient(self):
        self.absorption_leftend_coefficient = self._get_absorption_leftend_coefficient()

    def _get_absorption_leftend_coefficient(self):
        temp_term = sqrt(self.electric_field_update_coefficients_h[0] * self.magnetic_field_update_coefficients_e[0])
        return (temp_term - 1.0) / (temp_term + 1.0)

    def _set_absorption_rightend_coefficient(self):
        self.absorption_rightend_coefficient = self._get_absorption_rightend_coefficient()

    def _get_absorption_rightend_coefficient(self):
        temp_term = sqrt(
            self.electric_field_update_coefficients_h[self.mesh_size - 1] * self.magnetic_field_update_coefficients_e[
                self.mesh_size - 2])
        return (temp_term - 1.0) / (temp_term + 1.0)