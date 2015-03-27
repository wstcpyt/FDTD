__author__ = 'yutongpang'
import unittest
from unittest.mock import patch

import numpy as np
import numpy.testing as npt

from fdtdcode.field import Meshnodefield


class MeshnodefieldTest(unittest.TestCase):
    def setUp(self):
        self.meshnodefield = Meshnodefield(2)

    @patch.object(Meshnodefield, '_init_constant_and_variable')
    def test_init_meshnodefield(self, mock_init_constant_and_variable):
        self.meshnodefield = Meshnodefield(2)
        mock_init_constant_and_variable.assert_called_once_with(2)

    def test_init_constant_and_variable(self):
        self.assertEquals(self.meshnodefield.mesh_size, 2)
        self.assertEquals(len(self.meshnodefield.magnetic_field_y), 1)
        self.assertEquals(len(self.meshnodefield.electric_field_z), 2)
        self.assertEquals(len(self.meshnodefield.electric_field_update_coefficients_e), 2)
        self.assertEquals(len(self.meshnodefield.electric_field_update_coefficients_h), 2)

    def test_electric_node_size(self):
        size = len(self.meshnodefield.electric_field_z)
        self.assertEquals(size, self.meshnodefield.mesh_size)

    def test_magnetic_node_size(self):
        size = len(self.meshnodefield.magnetic_field_y)
        self.assertEquals(size, self.meshnodefield.mesh_size-1)

    @patch.object(Meshnodefield, '_update_magnetic_field_single_node')
    def test_update_magnetic_field_mesh(self, mock_update_magnetic_field):
        self.__initiate_meshnodefield_variable()
        mock_update_magnetic_field.return_value = 2.0
        result = self.meshnodefield.update_magnetic_field_mesh()
        npt.assert_array_equal(result, np.array([2.0, 2.0]))

    @patch.object(Meshnodefield, '_update_electric_field_single_node')
    def test_update_electric_field_mesh(self, mock_update_electric_field):
        self.__initiate_meshnodefield_variable()
        mock_update_electric_field.return_value = 2.0
        result = self.meshnodefield.update_electric_field_mesh()
        npt.assert_array_equal(result, np.array([2.0, 2.0, 2.0]))

    def test_meshnodefield_can_init_mesh_size(self):
        self.assertEqual(self.meshnodefield.mesh_size, 2)

    def test_absorption_boundary_condition_electric(self):
        self.__initiate_meshnodefield_variable()
        self.meshnodefield._set_electric_boundary_condition()
        result = self.meshnodefield.electric_field_z
        npt.assert_array_equal(result, np.array([2.0, 2.0, 2.0]))

    def test_update_magnetic_field_single_node(self):
        self.__initiate_meshnodefield_variable()
        result = self.meshnodefield._update_magnetic_field_single_node(1)
        self.assertEquals(2+1/self.meshnodefield.updatecoefficient, result)

    @patch.object(Meshnodefield, '_get_electric_field_update_coefficients_h')
    @patch.object(Meshnodefield, '_get_electric_field_update_coefficients_e')
    def test_update_electric_field_single_node(self, mock_get_electric_field_update_coefficients_e,
                                               mock_get_electric_field_update_coefficients_h):
        self.__initiate_meshnodefield_variable()
        mock_get_electric_field_update_coefficients_e.return_value = 2.0
        mock_get_electric_field_update_coefficients_h.return_value = 2.0
        result = self.meshnodefield._update_electric_field_single_node(1)
        mock_get_electric_field_update_coefficients_e.assert_called_once_with(1)
        mock_get_electric_field_update_coefficients_h.assert_called_once_with(1)
        self.assertEquals(2 * 2.0 + 1*2.0, result)

    @patch.object(Meshnodefield, '_get_electric_field_update_coefficients_h')
    @patch.object(Meshnodefield, '_get_electric_field_update_coefficients_e')
    def test_update_electric_field_single_node_call_function(self, mock_get_electric_field_update_coefficients_e,
                                                             mock_get_electric_field_update_coefficients_h):
        self.__initiate_meshnodefield_variable()
        self.meshnodefield._update_electric_field_single_node(1)
        mock_get_electric_field_update_coefficients_e.assert_called_once_with(1)
        mock_get_electric_field_update_coefficients_h.assert_called_once_with(1)

    def test_get_lossy_matrial_update_coefficient_electric(self):
        self.__initiate_meshnodefield_variable()
        self.meshnodefield.electric_field_update_coefficients_e = np.array([1, 2, 3])
        result = self.meshnodefield._get_electric_field_update_coefficients_e(1)
        self.assertEquals(2, result)

    def test_get_lossy_matrial_update_coefficient_magnetic(self):
        self.__initiate_meshnodefield_variable()
        self.meshnodefield.electric_field_update_coefficients_h = np.array([1, 2, 3])
        result = self.meshnodefield._get_electric_field_update_coefficients_h(1)
        self.assertEquals(2, result)

    def __initiate_meshnodefield_variable(self):
        self.meshnodefield.magnetic_field_y = np.array([1.0, 2.0])
        self.meshnodefield.electric_field_z = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.mesh_size = len(self.meshnodefield.electric_field_z)
