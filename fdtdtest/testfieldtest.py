__author__ = 'yutongpang'
import unittest
from unittest.mock import patch

import numpy as np
import numpy.testing as npt

from fdtdcode.field import Meshnodefield


class MeshnodefieldTest(unittest.TestCase):
    def setUp(self):
        self.meshnodefield = Meshnodefield(2)

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

    @patch.object(Meshnodefield, '_get_relative_permittivity')
    def test_update_electric_field_single_node(self, mock_get_relative_permittivity):
        self.__initiate_meshnodefield_variable()
        mock_get_relative_permittivity.return_value = 1
        result = self.meshnodefield._update_electric_field_single_node(1)
        self.assertEquals(2 + 1*self.meshnodefield.updatecoefficient, result)

    @patch.object(Meshnodefield, '_get_relative_permittivity')
    def test_update_electric_field_single_node_call_get_relative_permittivity_function(self,
                                                                                       mock_get_relative_permittivity):
        self.__initiate_meshnodefield_variable()
        mock_get_relative_permittivity.return_value = 1
        self.meshnodefield._update_electric_field_single_node(1)
        mock_get_relative_permittivity.assert_called_once_with(1)

    def test_get_relative_permittivity(self):
        self.__initiate_meshnodefield_variable()
        self.meshnodefield.relative_permittivity = np.array([1, 2, 3])
        result = self.meshnodefield._get_relative_permittivity(1)
        self.assertEquals(2, result)

    def __initiate_meshnodefield_variable(self):
        self.meshnodefield.magnetic_field_y = np.array([1.0, 2.0])
        self.meshnodefield.electric_field_z = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.mesh_size = len(self.meshnodefield.electric_field_z)
