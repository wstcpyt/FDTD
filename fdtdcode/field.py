__author__ = 'yutongpang'
import numpy as np


class Meshnodefield():
    def __init__(self, mesh_size):
        self.mesh_size = mesh_size
        self.magnetic_field_y = np.zeros(self.mesh_size - 1)
        self.electric_field_z = np.zeros(self.mesh_size)
        self.relative_permittivity = np.ones(mesh_size)

    updatecoefficient = 377

    def update_magnetic_field_mesh(self):
        for field_node_index in range(0, self.mesh_size-1):
            self.magnetic_field_y[field_node_index] = self.__update_magnetic_field_single_node(field_node_index)
        return self.magnetic_field_y

    def update_electric_field_mesh(self):
        self.__set_electric_boundary_condition()
        for field_node_index in range(1, self.mesh_size - 1):
            self.electric_field_z[field_node_index] = self.__update_electric_field_single_node(field_node_index)
        return self.electric_field_z

    def __set_electric_boundary_condition(self):
        self.electric_field_z[0] = self.electric_field_z[1]
        self.electric_field_z[self.mesh_size - 1] = self.electric_field_z[self.mesh_size - 2]

    def __update_magnetic_field_single_node(self, field_node_index):
        updatingterm = (self.electric_field_z[field_node_index+1] -
                        self.electric_field_z[field_node_index])/self.updatecoefficient
        updatedresult = self.magnetic_field_y[field_node_index] + updatingterm
        return updatedresult

    def __update_electric_field_single_node(self, field_node_index):
        relative_permittivity = self.__get_relative_permittivity(field_node_index)
        updatingterm = (self.magnetic_field_y[field_node_index] -
                        self.magnetic_field_y[field_node_index-1])*self.updatecoefficient/relative_permittivity
        updatedresult = self.electric_field_z[field_node_index] + updatingterm
        return updatedresult

    def __get_relative_permittivity(self, field_node_index):
        return self.relative_permittivity[field_node_index]