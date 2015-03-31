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
    def __init__(self, mesh_size, electric_field_update_coefficients_h, magnetic_field_update_coefficients_e):
        self._init_constant_and_variable(mesh_size, electric_field_update_coefficients_h,
                                         magnetic_field_update_coefficients_e)
        self._set_absorption_leftend_coefficient()
        self._set_absorption_rightend_coefficient()

    def _init_constant_and_variable(self, mesh_size, electric_field_update_coefficients_h,
                                    magnetic_field_update_coefficients_e):
        self.mesh_size = mesh_size
        self.electric_field_update_coefficients_h = electric_field_update_coefficients_h
        self.magnetic_field_update_coefficients_e = magnetic_field_update_coefficients_e
        self.electric_old_left = 0.0
        self.electric_old_right = 0.0

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

    def get_electric_field_at_left_end(self, electric_field_node_1, electric_field_node_0):
        result = self.electric_old_left + self.absorption_leftend_coefficient * (
            electric_field_node_1 - electric_field_node_0)
        self._set_electric_old_left(electric_field_node_1)
        return result

    def _set_electric_old_left(self, electric_field_node_1):
        self.electric_old_left = electric_field_node_1

    def get_electric_field_at_right_end(self, electric_field_node_meshsize_minus_2,
                                        electric_field_node_meshsize_minus_1):
        result = self.electric_old_right + self.absorption_rightend_coefficient * (
            electric_field_node_meshsize_minus_2 - electric_field_node_meshsize_minus_1)
        self._set_electric_old_right(electric_field_node_meshsize_minus_2)
        return result

    def _set_electric_old_right(self, electric_field_node_meshsize_minus_2):
        self.electric_old_right = electric_field_node_meshsize_minus_2