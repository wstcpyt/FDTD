__author__ = 'yutongpang'
import numpy as np


class Meshnodefield():
    def __init__(self, mesh_size):
        self._init_constant_and_variable(mesh_size)

    updatecoefficient = 377

    def _init_constant_and_variable(self, mesh_size):
        self.mesh_size = mesh_size
        self.magnetic_field_y = np.zeros(mesh_size - 1)
        self.electric_field_z = np.zeros(mesh_size)
        self.electric_field_update_coefficients_e = np.zeros(mesh_size)
        self.electric_field_update_coefficients_h = np.zeros(mesh_size)

    def update_magnetic_field_mesh(self):
        for field_node_index in range(0, self.mesh_size-1):
            self.magnetic_field_y[field_node_index] = self._update_magnetic_field_single_node(field_node_index)
        return self.magnetic_field_y

    def update_electric_field_mesh(self):
        self._set_electric_boundary_condition()
        for field_node_index in range(1, self.mesh_size - 1):
            self.electric_field_z[field_node_index] = self._update_electric_field_single_node(field_node_index)
        return self.electric_field_z

    def _set_electric_boundary_condition(self):
        self.electric_field_z[0] = self.electric_field_z[1]
        self.electric_field_z[self.mesh_size - 1] = self.electric_field_z[self.mesh_size - 2]

    def _update_magnetic_field_single_node(self, field_node_index):
        updatingterm = (self.electric_field_z[field_node_index+1] -
                        self.electric_field_z[field_node_index])/self.updatecoefficient
        updatedresult = self.magnetic_field_y[field_node_index] + updatingterm
        return updatedresult

    def _update_electric_field_single_node(self, field_node_index):
        electric_field_update_coefficients_e \
            = self._get_electric_field_update_coefficients_e(field_node_index)
        electric_field_update_coefficients_h \
            = self._get_electric_field_update_coefficients_h(field_node_index)
        updatingterm = (self.magnetic_field_y[field_node_index] -
                        self.magnetic_field_y[field_node_index-1])*electric_field_update_coefficients_h
        updatedresult = electric_field_update_coefficients_e*self.electric_field_z[field_node_index] + updatingterm
        return updatedresult

    def _get_electric_field_update_coefficients_e(self, field_node_index):
        return self.electric_field_update_coefficients_e[field_node_index]

    def _get_electric_field_update_coefficients_h(self, field_node_index):
        return self.electric_field_update_coefficients_h[field_node_index]