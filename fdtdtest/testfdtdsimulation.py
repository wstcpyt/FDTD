import sys
sys.path.append('/Users/yutongpang/PycharmProjects/FDTD')
import unittest
from unittest.mock import patch
import numpy.testing as npt
import numpy as np
from fdtdcode.fdtd_simulation import FDTDsimulation
from fdtdcode.field import Singlenodefield
from fdtdcode.source import Source


class FDTDsimulationTest(unittest.TestCase):
    def setUp(self):
        self.fdtdsimulation = FDTDsimulation(3, 2)

    def test_fdtdsimulation_can_init_mesh_size_and_max_time(self):
        self.assertEqual(self.fdtdsimulation.mesh_size, 3)
        self.assertEqual(self.fdtdsimulation.max_time, 2)

    @patch.object(Singlenodefield, 'update_magnetic_field')
    def test_envole_field_with_time_magnectic(self, mock_update_magnetic_field):
        self.__init_meshnode_field_in_fdtd_simulation()
        mock_update_magnetic_field.return_value = 2.0
        self.fdtdsimulation.envole_field_with_time()
        result = self.fdtdsimulation.magnetic_field_time
        npt.assert_array_equal(result, np.array([[2.0, 2.0, 2.0], [2.0, 2.0, 2.0]]))

    @patch.object(FDTDsimulation, '_FDTDsimulation__attach_additive_source')
    @patch.object(Singlenodefield, 'update_electric_field')
    def test_envole_field_with_time_electric(self, mock_update_electric_field, mock__FDTDsimulation__attach_additive_source):
        self.__init_meshnode_field_in_fdtd_simulation()
        mock__FDTDsimulation__attach_additive_source.return_value=0
        mock_update_electric_field.return_value = 2.0
        self.fdtdsimulation.envole_field_with_time()
        result = self.fdtdsimulation.electric_field_time
        npt.assert_array_equal(result, np.array([[2.0, 2.0, 2.0], [2.0, 2.0, 2.0]]))

    def __init_meshnode_field_in_fdtd_simulation(self):
        self.fdtdsimulation.meshnodefield.magnetic_field_y = np.array([1.0, 2.0, 3.0])
        self.fdtdsimulation.meshnodefield.electric_field_z = np.array([1.0, 2.0, 3.0])

    @patch.object(Source, 'get_additive_source_function_at_time_node_index')
    def test_additive_source_can_change_field_at_source_node_at_time_node_index(self, mock_source_function):
        mock_source_function.return_value = 50
        source_node = 1
        self.fdtdsimulation.source.source_node = source_node
        self.fdtdsimulation._FDTDsimulation__attach_additive_source(0)
        self.assertEqual(50, self.fdtdsimulation.meshnodefield.electric_field_z[source_node])


    def test_reshape_field_time(self):
        self.__initiate_fdtdsimulation_variable()
        self.fdtdsimulation._FDTDsimulation__reshape_field_time()
        result = self.fdtdsimulation.magnetic_field_time
        npt.assert_array_equal(result, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))

    def __initiate_fdtdsimulation_variable(self):
        self.fdtdsimulation.magnetic_field_time = np.array([1, 2, 3, 4, 5, 6])
        self.fdtdsimulation.electric_field_time = np.array([1, 2, 3, 4, 5, 6])
        self.fdtdsimulation.max_time = 2