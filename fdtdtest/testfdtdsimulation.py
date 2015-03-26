import unittest
from unittest.mock import patch
import numpy.testing as npt
import numpy as np
from fdtdcode.fdtd_simulation import FDTDsimulation
from fdtdcode.source import Source
from fdtdcode.boundaryconditon import TFSFboundarycondition


class FDTDsimulationTest(unittest.TestCase):
    def setUp(self):
        self.fdtdsimulation = FDTDsimulation(3, 2)

    def test_fdtdsimulation_can_init_mesh_size_and_max_time(self):
        self.assertEqual(self.fdtdsimulation.mesh_size, 3)
        self.assertEqual(self.fdtdsimulation.max_time, 2)

    @patch.object(FDTDsimulation, '_envole_magnetic_field')
    @patch.object(FDTDsimulation, '_envole_electric_field')
    @patch.object(FDTDsimulation, '_attach_additive_source')
    @patch.object(FDTDsimulation, '_apend_field_to_field_time_array')
    @patch.object(FDTDsimulation, '_reshape_field_time')
    def test_envole_field_with_time_electric(self, mock_reshape_field_time,
                                             mock_apend_field_to_field_time_array,
                                             mock_attach_additive_source,
                                             mock_envole_electric_field,
                                             mock_envole_magnetic_field
                                             ):
        self.fdtdsimulation.max_time = 1
        self.fdtdsimulation.envole_field_with_time()
        mock_reshape_field_time.assert_called_once_with()
        mock_apend_field_to_field_time_array.assert_called_once_with()
        mock_attach_additive_source.assert_called_once_with(0)
        mock_envole_electric_field.assert_called_once_with(0)
        mock_envole_magnetic_field.assert_called_once_with(0)

    @patch.object(Source, 'get_additive_source_function_at_time_node_index')
    def test_additive_source_can_change_field_at_source_node_at_time_node_index(self, mock_source_function):
        mock_source_function.return_value = 50
        source_node = 1
        self.fdtdsimulation.source.source_node = source_node
        self.fdtdsimulation._attach_additive_source(0)
        self.assertEqual(50, self.fdtdsimulation.meshnodefield.electric_field_z[source_node])

    @patch.object(FDTDsimulation, '_add_electric_tfsf_source_correction')
    def test_envole_electric_field_call_source_correction(self, mock_call_function):
        self.fdtdsimulation._envole_electric_field(0)
        mock_call_function.assert_called_once_with(0)

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