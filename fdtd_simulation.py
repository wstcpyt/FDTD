__author__ = 'yutongpang'
import numpy as np
from field import Meshnodefield

class FDTDsimulation():
    max_time = 2
    magnetic_field_time = np.array([])
    electric_field_time = np.array([])
    meshnodefield = Meshnodefield()

    def envole_field_with_time(self):
        for time_node_index in range(0, self.max_time):
            self.__envole_magnetic_field()
            self.__envole_electric_field()
        self.__reshape_field_time()

    def __reshape_field_time(self):
        row_length = self.max_time
        col_length = len(self.magnetic_field_time)/row_length
        self.magnetic_field_time = self.magnetic_field_time.reshape(row_length, col_length)
        self.electric_field_time = self.electric_field_time.reshape(row_length, col_length)

    def __envole_electric_field(self):
        meshelectric_field_current_time = self.meshnodefield.update_electric_field_mesh()
        self.electric_field_time = np.append(self.electric_field_time, meshelectric_field_current_time)

    def __envole_magnetic_field(self):
        meshmagnetic_field_current_time = self.meshnodefield.update_magnetic_field_mesh()
        self.magnetic_field_time = np.append(self.magnetic_field_time, meshmagnetic_field_current_time)