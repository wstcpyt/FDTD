__author__ = 'yutongpang'
import unittest
import numpy as np
from unittest.mock import patch
from fdtdcode.structure import Structureparameter
from fdtdcode.field import Meshnodefield


class PermittivityTEST(unittest.TestCase):
    def setUp(self):
        self.structureparameter = Structureparameter(190)

    @patch.object(Structureparameter, '_set_electric_field_update_coefficients_H')
    @patch.object(Structureparameter, '_set_electric_field_update_coefficients_E')
    @patch.object(Structureparameter, '_set_relative_permittivity')
    def test_init_structure_permittivity(self, mock_set_relative_permittivity,
                                         mock_set_electric_field_update_coefficients_E,
                                         mock_set_electric_field_update_coefficients_H):
        self.structureparameter = Structureparameter(100)
        mock_set_relative_permittivity.return_value = np.ones(self.structureparameter.mesh_size)
        mock_set_relative_permittivity.assert_called_once_with()
        mock_set_electric_field_update_coefficients_E.assert_called_once_with()
        mock_set_electric_field_update_coefficients_H.assert_called_once_with()

    @patch.object(Structureparameter, '_get_relative_permittivity_in_single_node')
    def test_set_relative_permittivity(self, mock_get_relative_permittivity_in_single_node):
        returnvalue = self.structureparameter._set_relative_permittivity()
        length = len(returnvalue)
        self.assertEquals(length, self.structureparameter.mesh_size)
        callcount = mock_get_relative_permittivity_in_single_node.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_relative_permittivity_in_single_node(self):
        returnvalue_node_less_100 = self.structureparameter._get_relative_permittivity_in_single_node(50)
        self.assertEquals(returnvalue_node_less_100, 1)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_relative_permittivity_in_single_node(150)
        self.assertEquals(returnvalue_node_equal_or_more_100, 9)

    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_E')
    def test_set_lossy_matrial_update_coefficient_electric(self, mock_electric_field_update_coefficients_E):
        returnvalue = self.structureparameter._set_electric_field_update_coefficients_E()
        length = len(returnvalue)
        self.assertEquals(length, self.structureparameter.mesh_size)
        callcount = mock_electric_field_update_coefficients_E.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_lossy_matrial_update_coefficient_electric(self):
        returnvalue_node_less_100 = self.structureparameter._get_electric_field_update_coefficients_E(50)
        self.assertEquals(returnvalue_node_less_100, 1.0)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_electric_field_update_coefficients_E(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          (1.0 - self.structureparameter.loss)/(1.0 + self.structureparameter.loss))

    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_H')
    def test_set_lossy_matrial_update_coefficient_magnetic(self, mock_electric_field_update_coefficients_H):
        returnvalue = self.structureparameter._set_electric_field_update_coefficients_H()
        length = len(returnvalue)
        self.assertEquals(length, self.structureparameter.mesh_size)
        callcount = mock_electric_field_update_coefficients_H.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_lossy_matrial_update_coefficient_magnetic(self):
        returnvalue_node_less_100 = self.structureparameter._get_electric_field_update_coefficients_H(50)
        self.assertEquals(returnvalue_node_less_100, Meshnodefield.updatecoefficient)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_electric_field_update_coefficients_H(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          Meshnodefield.updatecoefficient/self.structureparameter.relative_permittivity[150]/(1.0+self.structureparameter.loss))