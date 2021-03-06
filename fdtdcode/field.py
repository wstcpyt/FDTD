__author__ = 'yutongpang'
import numpy as np
from fdtdcode.structure import Structureparameter


class Meshnodefield():
    def __init__(self, mesh_size):
        self._init_constant_and_variable(mesh_size)
        self.structureparameter = Structureparameter(mesh_size)

    updatecoefficient = 377
    courant_number = 1.0

    def _init_constant_and_variable(self, mesh_size):
        self.mesh_size = mesh_size
        self.magnetic_field_y = np.zeros(mesh_size - 1)
        self.electric_field_z = np.zeros(mesh_size)

    def update_magnetic_field_mesh(self):
        for field_node_index in range(0, self.mesh_size - 1):
            self.magnetic_field_y[field_node_index] = self._update_magnetic_field_single_node(field_node_index)
        return self.magnetic_field_y

    def update_electric_field_mesh(self):
        for field_node_index in range(1, self.mesh_size - 1):
            self.electric_field_z[field_node_index] = self._update_electric_field_single_node(field_node_index)
        return self.electric_field_z

    def _update_magnetic_field_single_node(self, field_node_index):
        magnetic_field_update_coefficients_e = self._get_magnetic_field_update_coefficients_e(field_node_index)
        magnetic_field_update_coefficients_h = self._get_magnetic_field_update_coefficients_h(field_node_index)
        updatingterm = (self.electric_field_z[field_node_index + 1] -
                        self.electric_field_z[field_node_index]) * magnetic_field_update_coefficients_e
        updatedresult = self.magnetic_field_y[field_node_index] * magnetic_field_update_coefficients_h + updatingterm
        return updatedresult

    def _get_magnetic_field_update_coefficients_e(self, field_node_index):
        return self.structureparameter.magnetic_field_update_coefficients_e[field_node_index]

    def _get_magnetic_field_update_coefficients_h(self, field_node_index):
        return self.structureparameter.magnetic_field_update_coefficients_h[field_node_index]

    def _update_electric_field_single_node(self, field_node_index):
        electric_field_update_coefficients_e \
            = self._get_electric_field_update_coefficients_e(field_node_index)
        electric_field_update_coefficients_h \
            = self._get_electric_field_update_coefficients_h(field_node_index)
        updatingterm = (self.magnetic_field_y[field_node_index] -
                        self.magnetic_field_y[field_node_index - 1]) * electric_field_update_coefficients_h
        updatedresult = electric_field_update_coefficients_e * self.electric_field_z[field_node_index] + updatingterm
        return updatedresult

    def _get_electric_field_update_coefficients_e(self, field_node_index):
        return self.structureparameter.electric_field_update_coefficients_e[field_node_index]

    def _get_electric_field_update_coefficients_h(self, field_node_index):
        return self.structureparameter.electric_field_update_coefficients_h[field_node_index]