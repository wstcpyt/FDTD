__author__ = 'yutongpang'
import numpy as np


class Meshnodefield():
    def __init__(self, mesh_size):
        self.mesh_size = mesh_size
        self.magnetic_field_y = np.zeros(self.mesh_size)
        self.electric_field_z = np.zeros(self.mesh_size)

    def update_magnetic_field_mesh(self):
        self.__set_magnetic_boundary_condition()
        for field_node_index in range(0, self.mesh_size-1):
            self.magnetic_field_y[field_node_index] = \
                Singlenodefield.update_magnetic_field(self.magnetic_field_y[field_node_index],
                                                      self.electric_field_z[field_node_index],
                                                      self.electric_field_z[field_node_index+1])
        return self.magnetic_field_y

    def update_electric_field_mesh(self):
        self.__set_electric_boundary_condition()
        for field_node_index in range(1, self.mesh_size):
            self.electric_field_z[field_node_index] = \
                Singlenodefield.update_electric_field(self.electric_field_z[field_node_index],
                                                      self.magnetic_field_y[field_node_index-1],
                                                      self.magnetic_field_y[field_node_index])
        return self.electric_field_z

    def __set_electric_boundary_condition(self):
        self.electric_field_z[0] = self.electric_field_z[1]

    def __set_magnetic_boundary_condition(self):
        self.magnetic_field_y[self.mesh_size-1] = self.magnetic_field_y[self.mesh_size-2]


class Singlenodefield():
    updatecoefficient = 377

    @classmethod
    def update_magnetic_field(cls, h_field_in_current_node, e_field_in_current_node, e_field_in_next_node):
        updatingterm = (e_field_in_next_node - e_field_in_current_node)/cls.updatecoefficient
        updatedresult = h_field_in_current_node + updatingterm
        return updatedresult

    @classmethod
    def update_electric_field(cls, e_field_in_current_node, h_field_in_previous_node, h_field_in_current_node):
        updatingterm = (h_field_in_current_node-h_field_in_previous_node)*cls.updatecoefficient
        updatedresult = e_field_in_current_node + updatingterm
        return updatedresult
