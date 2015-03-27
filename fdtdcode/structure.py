__author__ = 'yutongpang'
import numpy as np
from fdtdcode.field import Meshnodefield


class Structureparameter():
    def __init__(self, mesh_size):
        self.mesh_size = mesh_size
        self.loss = 0.01
        self.relative_permittivity = self._set_relative_permittivity()
        self.electric_field_update_coefficients_E = self._set_electric_field_update_coefficients_E()
        self.electric_field_update_coefficients_H = self._set_electric_field_update_coefficients_H()

    def _set_relative_permittivity(self):
        relative_permittivity = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            relative_permittivity[field_node_index] = self._get_relative_permittivity_in_single_node(field_node_index)
        return relative_permittivity

    def _set_electric_field_update_coefficients_E(self):
        electric_field_update_coefficients_E = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            electric_field_update_coefficients_E[field_node_index] \
                = self._get_electric_field_update_coefficients_E(field_node_index)
        return electric_field_update_coefficients_E

    def _set_electric_field_update_coefficients_H(self):
        electric_field_update_coefficients_H = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            electric_field_update_coefficients_H[field_node_index] \
                = self._get_electric_field_update_coefficients_H(field_node_index)
        return electric_field_update_coefficients_H

    def _get_electric_field_update_coefficients_H(self, field_node_index):
        if field_node_index < 100:
            return Meshnodefield.updatecoefficient
        else:
            return Meshnodefield.updatecoefficient/self.relative_permittivity[field_node_index]/(1.0 + self.loss)

    def _get_electric_field_update_coefficients_E(self, field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return (1.0 - self.loss)/(1.0 + self.loss)

    @staticmethod
    def _get_relative_permittivity_in_single_node(field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return 9.0