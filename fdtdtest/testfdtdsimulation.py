import unittest
from unittest.mock import patch
import numpy.testing as npt
import numpy as np
from fdtdcode.fdtd_simulation import FDTDsimulation
from fdtdcode.boundaryconditon import TFSFboundarycondition, Absorption
from fdtdcode.field import Meshnodefield


class FDTDsimulationTest(unittest.TestCase):
    def setUp(self):
        self.fdtdsimulation = FDTDsimulation(3, 2)

    @patch.object(FDTDsimulation, '_init_constant_and_variable')
    def test_init_fdtdsimulation(self, mock_init_constant_and_variable):
        self.fdtdsimulation = FDTDsimulation(3, 2)
        mock_init_constant_and_variable.assert_called_once_with(3, 2)

    def test_init_constant_and_variable(self):
        self.assertEquals(self.fdtdsimulation.mesh_size, 3)
        self.assertEquals(self.fdtdsimulation.max_time, 2)
        self.assertEquals(len(self.fdtdsimulation.magnetic_field_time), 0)
        self.assertEquals(len(self.fdtdsimulation.electric_field_time), 0)

    @patch.object(FDTDsimulation, '_envole_magnetic_field')
    @patch.object(FDTDsimulation, '_envole_electric_field')
    @patch.object(FDTDsimulation, '_apend_field_to_field_time_array')
    @patch.object(FDTDsimulation, '_reshape_field_time')
    def test_envole_field_with_time_electric(self, mock_reshape_field_time,
                                             mock_apend_field_to_field_time_array,
                                             mock_envole_electric_field,
                                             mock_envole_magnetic_field
                                             ):
        self.fdtdsimulation.max_time = 1
        self.fdtdsimulation.envole_field_with_time()
        mock_reshape_field_time.assert_called_once_with()
        mock_apend_field_to_field_time_array.assert_called_once_with()
        mock_envole_electric_field.assert_called_once_with(0)
        mock_envole_magnetic_field.assert_called_once_with(0)

    @patch.object(FDTDsimulation, '_set_absorption_boundary_condition')
    @patch.object(Meshnodefield, 'update_electric_field_mesh')
    @patch.object(FDTDsimulation, '_add_electric_tfsf_source_correction')
    def test_envole_electric_field_call_source_correction(self, mock_add_electric_tfsf_source_correction,
                                                          mock_update_electric_field_mesh,
                                                          mock_set_absorption_boundary_condition):
        self.fdtdsimulation._envole_electric_field(0)
        mock_add_electric_tfsf_source_correction.assert_called_once_with(0)
        mock_update_electric_field_mesh.assert_called_once_with()
        mock_set_absorption_boundary_condition.assert_called_once_with()

    @patch.object(Absorption, 'get_electric_field_at_right_end')
    @patch.object(Absorption, 'get_electric_field_at_left_end')
    def test_set_absorption_boundary_condition(self, mock_get_electric_field_at_left_end, mock_get_electric_field_at_right_end):
        mock_get_electric_field_at_right_end.return_value = 2.0
        mock_get_electric_field_at_left_end.return_value = 2.0
        self.fdtdsimulation._set_absorption_boundary_condition()
        mock_get_electric_field_at_left_end.assert_called_once_with(0.0, 0.0)
        mock_get_electric_field_at_right_end.assert_called_once_with(2.0, 0.0)
        self.assertEquals(self.fdtdsimulation.meshnodefield.electric_field_z[0], 2.0)
        self.assertEquals(self.fdtdsimulation.meshnodefield.electric_field_z[2], 2.0)

    @patch.object(FDTDsimulation, '_add_magnetic_tfsf_source_correction')
    def test_envole_magnetic_field_call_source_correction(self, mock_call_function):
        self.fdtdsimulation._envole_magnetic_field(0)
        mock_call_function.assert_called_once_with(0)

    @patch.object(TFSFboundarycondition, 'get_incidence_source_correction')
    def test_add_magnetic_tfsf_source_correction(self, mock_get_incidence_source_correction):
        mock_get_incidence_source_correction.return_value = 1
        self.fdtdsimulation.meshnodefield.magnetic_field_y[1] = 0
        self.fdtdsimulation.tfsfboundarycondition.magnetic_tfsf_node_index = 1
        self.fdtdsimulation._add_magnetic_tfsf_source_correction(0)
        mock_get_incidence_source_correction.assert_called_once_with(0, 0)
        self.assertEquals(self.fdtdsimulation.meshnodefield.magnetic_field_y[1], -1)

    @patch.object(TFSFboundarycondition, 'get_incidence_source_correction')
    def test_add_electric_tfsf_source_correction(self, mock_get_incidence_source_correction):
        mock_get_incidence_source_correction.return_value = 1
        self.fdtdsimulation.meshnodefield.electric_field_z[2] = 0
        self.fdtdsimulation.tfsfboundarycondition.magnetic_tfsf_node_index = 1
        self.fdtdsimulation._add_electric_tfsf_source_correction(0)
        mock_get_incidence_source_correction.assert_called_once_with(0, 1)
        self.assertEquals(self.fdtdsimulation.meshnodefield.electric_field_z[2], 1)

    def test_reshape_field_time(self):
        self.__initiate_fdtdsimulation_variable()
        self.fdtdsimulation._reshape_field_time()
        result = self.fdtdsimulation.electric_field_time
        npt.assert_array_equal(result, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))

    def __initiate_fdtdsimulation_variable(self):
        self.fdtdsimulation.magnetic_field_time = np.array([1, 2, 3, 4])
        self.fdtdsimulation.electric_field_time = np.array([1, 2, 3, 4, 5, 6])
        self.fdtdsimulation.max_time = 2

    def test_apend_field_to_field_time_array(self):
        self.fdtdsimulation.electric_field_time = np.array([1, 2, 3])
        self.fdtdsimulation.magnetic_field_time = np.array([1, 2, 3])
        self.fdtdsimulation.meshnodefield.electric_field_z = np.array([1, 2, 3])
        self.fdtdsimulation.meshnodefield.magnetic_field_y = np.array([1, 2, 3])
        self.fdtdsimulation._apend_field_to_field_time_array()
        npt.assert_array_equal(self.fdtdsimulation.electric_field_time, np.array([1, 2, 3, 1, 2, 3]))
        npt.assert_array_equal(self.fdtdsimulation.magnetic_field_time, np.array([1, 2, 3, 1, 2, 3]))
