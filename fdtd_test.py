__author__ = 'yutongpang'
import unittest
from field import Singlenodefield, Meshnodefield
from fdtd_simulation import FDTDsimulation
import numpy.testing as npt
import numpy as np
from unittest.mock import patch


class FDTDsimulationTest(unittest.TestCase):
    def setUp(self):
        self.fdtdsimulation = FDTDsimulation()

    @patch.object(Meshnodefield, 'update_magnetic_field_mesh')
    def test_envole_field_with_time_magnectic(self, mock_update_magnetic_field_mesh):
        mock_update_magnetic_field_mesh.return_value = np.array([2.0, 2.0, 3.0])
        self.fdtdsimulation.envole_field_with_time()
        expectedresult = self.fdtdsimulation.magnetic_field_time
        npt.assert_array_equal(expectedresult, np.array([[2.0, 2.0, 3.0], [2.0, 2.0, 3.0]]))

    @patch.object(Meshnodefield, 'update_electric_field_mesh')
    def test_envole_field_with_time_electric(self, mock_update_electric_field_mesh):
        mock_update_electric_field_mesh.return_value = np.array([1.0, 2.0, 2.0])
        self.fdtdsimulation.envole_field_with_time()
        expectedresult = self.fdtdsimulation.electric_field_time
        npt.assert_array_equal(expectedresult, np.array([[1.0, 2.0, 2.0], [1.0, 2.0, 2.0]]))

    def test_reshape_field_time(self):
        self.__initiate_fdtdsimulation_variable()
        self.fdtdsimulation._FDTDsimulation__reshape_field_time()
        expectedvalue = self.fdtdsimulation.magnetic_field_time
        npt.assert_array_equal(expectedvalue, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))

    def __initiate_fdtdsimulation_variable(self):
        self.fdtdsimulation.magnetic_field_time = np.array([1, 2, 3, 4, 5, 6])
        self.fdtdsimulation.electric_field_time = np.array([1, 2, 3, 4, 5, 6])
        self.fdtdsimulation.max_time = 2

class MeshnodefieldTest(unittest.TestCase):
    def setUp(self):
        self.meshnodefield = Meshnodefield()

    @patch.object(Singlenodefield, 'update_magnetic_field')
    def test_update_magnetic_field_mesh(self, mock_update_magnetic_field):
        self.__initiate_meshnodefield_variable()
        mock_update_magnetic_field.return_value = 2.0
        expectedresult = self.meshnodefield.update_magnetic_field_mesh()
        npt.assert_array_equal(expectedresult, np.array([2.0, 2.0, 3.0]))

    @patch.object(Meshnodefield, '_Meshnodefield__set_source_condition')
    @patch.object(Singlenodefield, 'update_electric_field')
    def test_update_electric_field_mesh(self, mock_update_electric_field, mock_Meshnodefield__set_source_condition):
        self.__initiate_meshnodefield_variable()
        mock_Meshnodefield__set_source_condition.return_value = None
        mock_update_electric_field.return_value = 2.0
        expectedresult = self.meshnodefield.update_electric_field_mesh()
        npt.assert_array_equal(expectedresult, np.array([1.0, 2.0, 2.0]))

    @patch.object(Singlenodefield, 'update_electric_field')
    def test_update_electric_field_mesh_with_source(self, mock_update_electric_field):
        mock_update_electric_field.return_value = 2.0


    def __initiate_meshnodefield_variable(self):
        self.meshnodefield.magnetic_field_y = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.electric_field_z = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.mesh_size = len(self.meshnodefield.electric_field_z)

class SinglenodefieldTEST(unittest.TestCase):
    def setUp(self):
        self.singlenodefiled = Singlenodefield()
        self.updatingcoeffiecient = self.singlenodefiled.updatecoefficient

    def test_update_magnetic_field(self):
        expectedresult = self.singlenodefiled.update_magnetic_field(0, 0, 1)
        self.assertEqual(expectedresult, 1/self.updatingcoeffiecient)

    def test_update_electric_field(self):
        expectedresult = self.singlenodefiled.update_electric_field(0, 0, 1)
        self.assertEqual(expectedresult, 1*self.updatingcoeffiecient)