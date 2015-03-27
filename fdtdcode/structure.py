__author__ = 'yutongpang'
import numpy as np


class Structureparameter():
    def __init__(self, mesh_size):
        self._init_constant_and_variable(mesh_size)
        self._set_relative_permittivity()
        self._set_electric_field_update_coefficients()

    updatecoefficient = 377

    def _init_constant_and_variable(self, mesh_size):
        self.loss = 0.01
        self.mesh_size = mesh_size

    def _set_relative_permittivity(self):
        self.relative_permittivity = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            self.relative_permittivity[field_node_index] = self._get_relative_permittivity_in_single_node(
                field_node_index)

    @staticmethod
    def _get_relative_permittivity_in_single_node(field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return 9.0

    def _set_electric_field_update_coefficients(self):
        self.electric_field_update_coefficients_e = np.zeros(self.mesh_size)
        self.electric_field_update_coefficients_h = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            self.electric_field_update_coefficients_e[field_node_index] \
                = self._get_electric_field_update_coefficients_e(field_node_index)
            self.electric_field_update_coefficients_h[field_node_index] \
                = self._get_electric_field_update_coefficients_h(field_node_index)

    def _get_electric_field_update_coefficients_h(self, field_node_index):
        if field_node_index < 100:
            return self.updatecoefficient
        else:
            return self.updatecoefficient / self.relative_permittivity[field_node_index] / (1.0 + self.loss)

    def _get_electric_field_update_coefficients_e(self, field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return (1.0 - self.loss) / (1.0 + self.loss)