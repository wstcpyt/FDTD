__author__ = 'yutongpang'
import numpy as np
from field import Meshnodefield

class FDTDsimulation():
    def __init__(self, mesh_size, max_time):
        self.mesh_size = mesh_size
        self.max_time = max_time
        self.meshnodefield = Meshnodefield(mesh_size)

    magnetic_field_time = np.array([])
    electric_field_time = np.array([])

    def envole_field_with_time(self):
        for time_node_index in range(0, self.max_time):
            self.__envole_magnetic_field()
            self.__envole_electric_field(time_node_index)
        self.__reshape_field_time()

    def __reshape_field_time(self):
        row_length = self.max_time
        col_length = len(self.magnetic_field_time)/row_length
        self.magnetic_field_time = self.magnetic_field_time.reshape(row_length, col_length)
        self.electric_field_time = self.electric_field_time.reshape(row_length, col_length)

    def __envole_electric_field(self, time_node_index):
        meshelectric_field_current_time = self.meshnodefield.update_electric_field_mesh(time_node_index)
        self.electric_field_time = np.append(self.electric_field_time, meshelectric_field_current_time)

    def __envole_magnetic_field(self):
        meshmagnetic_field_current_time = self.meshnodefield.update_magnetic_field_mesh()
        self.magnetic_field_time = np.append(self.magnetic_field_time, meshmagnetic_field_current_time)