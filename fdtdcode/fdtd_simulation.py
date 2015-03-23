__author__ = 'yutongpang'
import numpy as np
from fdtdcode.field import Meshnodefield
from fdtdcode.source import Source


class FDTDsimulation():
    def __init__(self, mesh_size, max_time):
        self.mesh_size = mesh_size
        self.max_time = max_time
        self.meshnodefield = Meshnodefield(mesh_size)
        self.source = Source(0)

    magnetic_field_time = np.array([])
    electric_field_time = np.array([])

    def envole_field_with_time(self):
        for time_node_index in range(0, self.max_time):
            self.__envole_magnetic_field()
            self.__envole_electric_field()
            self.__attach_additive_source(time_node_index)
            self.__apend_field_to_field_time_array()
        self.__reshape_field_time()

    def __reshape_field_time(self):
        row_length = self.max_time
        col_length = len(self.magnetic_field_time)/row_length
        self.magnetic_field_time = self.magnetic_field_time.reshape(row_length, col_length)
        self.electric_field_time = self.electric_field_time.reshape(row_length, col_length)

    def __envole_electric_field(self):
        self.meshnodefield.update_electric_field_mesh()

    def __envole_magnetic_field(self):
        self.meshnodefield.update_magnetic_field_mesh()

    def __apend_field_to_field_time_array(self):
        self.electric_field_time = np.append(self.electric_field_time, self.meshnodefield.electric_field_z)
        self.magnetic_field_time = np.append(self.magnetic_field_time, self.meshnodefield.magnetic_field_y)

    def __attach_additive_source(self, time_node_index):
        field_at_source_node = self.source.get_additive_source_function_at_time_node_index(time_node_index)
        self.meshnodefield.electric_field_z[self.source.source_node] = field_at_source_node
