__author__ = 'yutongpang'
import unittest
import numpy as np
from unittest.mock import patch
from fdtdcode.structure import Structureparameter
from fdtdcode.field import Meshnodefield


class PermittivityTEST(unittest.TestCase):
    def setUp(self):
        self.structureparameter = Structureparameter(190)

    @patch.object(Structureparameter, '_init_constant_and_variable')
    @patch.object(Structureparameter, '_set_electric_field_update_coefficients')
    @patch.object(Structureparameter, '_set_relative_permittivity')
    def test_init_structure_permittivity(self, mock_set_relative_permittivity,
                                         mock_set_electric_field_update_coefficients,
                                         mock_init_constant_and_variable):
        self.structureparameter = Structureparameter(190)
        mock_set_relative_permittivity.return_value = np.ones(190)
        mock_set_relative_permittivity.assert_called_once_with()
        mock_set_electric_field_update_coefficients.assert_called_once_with()
        mock_init_constant_and_variable.assert_called_once_with(190)

    def test_init_constant_and_variable(self):
        self.assertEquals(self.structureparameter.mesh_size, 190)
        self.assertEquals(self.structureparameter.loss, 0.01)

    @patch.object(Structureparameter, '_get_relative_permittivity_in_single_node')
    def test_set_relative_permittivity(self, mock_get_relative_permittivity_in_single_node):
        self.structureparameter._set_relative_permittivity()
        callcount = mock_get_relative_permittivity_in_single_node.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_relative_permittivity_in_single_node(self):
        returnvalue_node_less_100 = self.structureparameter._get_relative_permittivity_in_single_node(50)
        self.assertEquals(returnvalue_node_less_100, 1)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_relative_permittivity_in_single_node(150)
        self.assertEquals(returnvalue_node_equal_or_more_100, 9)

    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_h')
    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_e')
    def test_set_lossy_matrial_update_coefficient_electric(self, mock_electric_field_update_coefficients_e,
                                                           mock_electric_field_update_coefficients_h):
        self.structureparameter._set_electric_field_update_coefficients()
        callcount_E = mock_electric_field_update_coefficients_e.call_count
        callcount_H = mock_electric_field_update_coefficients_h.call_count
        self.assertEqual(callcount_E, callcount_H)
        self.assertEquals(callcount_E, self.structureparameter.mesh_size)

    def test_get_lossy_matrial_update_coefficient_electric(self):
        returnvalue_node_less_100 = self.structureparameter._get_electric_field_update_coefficients_e(50)
        self.assertEquals(returnvalue_node_less_100, 1.0)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_electric_field_update_coefficients_e(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          (1.0 - self.structureparameter.loss)/(1.0 + self.structureparameter.loss))

    def test_get_lossy_matrial_update_coefficient_magnetic(self):
        returnvalue_node_less_100 = self.structureparameter._get_electric_field_update_coefficients_h(50)
        self.assertEquals(returnvalue_node_less_100, Meshnodefield.updatecoefficient)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_electric_field_update_coefficients_h(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          Meshnodefield.updatecoefficient/self.structureparameter.relative_permittivity[150]/(1.0+self.structureparameter.loss))