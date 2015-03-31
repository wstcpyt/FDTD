__author__ = 'yutongpang'
import numpy as np
from fdtdcode.field import Meshnodefield
from fdtdcode.boundaryconditon import TFSFboundarycondition, Absorption


class FDTDsimulation():
    def __init__(self, mesh_size, max_time):
        self._init_constant_and_variable(mesh_size, max_time)
        self.meshnodefield = Meshnodefield(mesh_size)
        self.tfsfboundarycondition = TFSFboundarycondition(0)
        self.absorption = Absorption(mesh_size,
                                     self.meshnodefield.structureparameter.electric_field_update_coefficients_h,
                                     self.meshnodefield.structureparameter.magnetic_field_update_coefficients_e)

    def _init_constant_and_variable(self, mesh_size, max_time):
        self.mesh_size = mesh_size
        self.max_time = max_time
        self.magnetic_field_time = np.array([])
        self.electric_field_time = np.array([])

    def envole_field_with_time(self):
        for time_node_index in range(0, self.max_time):
            self._envole_magnetic_field(time_node_index)
            self._envole_electric_field(time_node_index)
            self._apend_field_to_field_time_array()
        self._reshape_field_time()

    def _reshape_field_time(self):
        row_length = self.max_time
        col_length_electric = len(self.electric_field_time) / row_length
        col_length_magnetic = len(self.magnetic_field_time) / row_length
        self.magnetic_field_time = self.magnetic_field_time.reshape(row_length, col_length_magnetic)
        self.electric_field_time = self.electric_field_time.reshape(row_length, col_length_electric)

    def _envole_electric_field(self, time_node_index):
        self._add_electric_tfsf_source_correction(time_node_index)
        self.meshnodefield.update_electric_field_mesh()
        self._set_absorption_boundary_condition()

    def _set_absorption_boundary_condition(self):
        self.meshnodefield.electric_field_z[0] = self.absorption.get_electric_field_at_left_end(
            self.meshnodefield.electric_field_z[1], self.meshnodefield.electric_field_z[0])
        self.meshnodefield.electric_field_z[self.mesh_size - 1] = self.absorption.get_electric_field_at_right_end(
            self.meshnodefield.electric_field_z[self.mesh_size - 2],
            self.meshnodefield.electric_field_z[self.mesh_size - 1])

    def _envole_magnetic_field(self, time_node_index):
        self.meshnodefield.update_magnetic_field_mesh()
        self._add_magnetic_tfsf_source_correction(time_node_index)

    def _add_magnetic_tfsf_source_correction(self, time_node_index):
        correction_term = self.tfsfboundarycondition.get_incidence_source_correction(time_node_index, 0)
        self.meshnodefield.magnetic_field_y[self.tfsfboundarycondition.magnetic_tfsf_node_index] -= correction_term

    def _add_electric_tfsf_source_correction(self, time_node_index):
        correction_term = self.tfsfboundarycondition.get_incidence_source_correction(time_node_index, 1)
        self.meshnodefield.electric_field_z[self.tfsfboundarycondition.magnetic_tfsf_node_index + 1] += correction_term

    def _apend_field_to_field_time_array(self):
        self.electric_field_time = np.append(self.electric_field_time, self.meshnodefield.electric_field_z)
        self.magnetic_field_time = np.append(self.magnetic_field_time, self.meshnodefield.magnetic_field_y)
