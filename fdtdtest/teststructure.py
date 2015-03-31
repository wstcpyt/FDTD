__author__ = 'yutongpang'
import unittest
import numpy as np
from unittest.mock import patch
from fdtdcode.structure import Structureparameter
from fdtdcode.field import Meshnodefield


class PermittivityTEST(unittest.TestCase):
    def setUp(self):
        self.structureparameter = Structureparameter(190)

    @patch.object(Structureparameter, '_set_magnetic_field_update_coefficients')
    @patch.object(Structureparameter, '_init_constant_and_variable')
    @patch.object(Structureparameter, '_set_electric_field_update_coefficients')
    @patch.object(Structureparameter, '_set_relative_permittivity')
    def test_init_structure_permittivity(self, mock_set_relative_permittivity,
                                         mock_set_electric_field_update_coefficients,
                                         mock_init_constant_and_variable,
                                         mock_set_magnetic_field_update_coefficients):
        self.structureparameter = Structureparameter(190)
        mock_set_relative_permittivity.return_value = np.ones(190)
        mock_set_relative_permittivity.assert_called_once_with()
        mock_set_electric_field_update_coefficients.assert_called_once_with()
        mock_set_magnetic_field_update_coefficients.assert_called_once_with()
        mock_init_constant_and_variable.assert_called_once_with(190)

    def test_init_constant_and_variable(self):
        self.assertEquals(self.structureparameter.mesh_size, 190)
        self.assertEquals(self.structureparameter.loss, 0)
        self.assertEqual(self.structureparameter.loss_layer, 100)

    @patch.object(Structureparameter, '_get_relative_permittivity_in_single_node')
    def test_set_relative_permittivity(self, mock_get_relative_permittivity_in_single_node):
        self.structureparameter._set_relative_permittivity()
        callcount = mock_get_relative_permittivity_in_single_node.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_relative_permittivity_in_single_node(self):
        returnvalue_node_less_100 = self.structureparameter._get_relative_permittivity_in_single_node(50)
        self.assertEquals(returnvalue_node_less_100, 1)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_relative_permittivity_in_single_node(150)
        self.assertEquals(returnvalue_node_equal_or_more_100, 4.0)

    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_h')
    @patch.object(Structureparameter, '_get_electric_field_update_coefficients_e')
    def test_set_electric_field_update_coefficients(self, mock_electric_field_update_coefficients_e,
                                                    mock_electric_field_update_coefficients_h):
        self.structureparameter._set_electric_field_update_coefficients()
        callcount_E = mock_electric_field_update_coefficients_e.call_count
        callcount_H = mock_electric_field_update_coefficients_h.call_count
        self.assertEqual(callcount_E, callcount_H)
        self.assertEquals(callcount_E, self.structureparameter.mesh_size)

    def test_get_electric_field_update_coefficients_e(self):
        returnvalue_node_less_loss_layer = self.structureparameter._get_electric_field_update_coefficients_e(
            self.structureparameter.loss_layer - 1)
        self.assertEquals(returnvalue_node_less_loss_layer, 1.0)
        returnvalue_node_more_loss_layer = self.structureparameter._get_electric_field_update_coefficients_e(
            self.structureparameter.loss_layer + 1)
        self.assertEquals(returnvalue_node_more_loss_layer,
                          (1.0 - self.structureparameter.loss) / (1.0 + self.structureparameter.loss))

    def test_get_electric_field_update_coefficients_h(self):
        returnvalue_node_less_loss_layer = self.structureparameter._get_electric_field_update_coefficients_h(
            self.structureparameter.loss_layer - 1)
        self.assertEqual(returnvalue_node_less_loss_layer,
                         Meshnodefield.updatecoefficient / self.structureparameter.relative_permittivity[
                             self.structureparameter.loss_layer - 1])
        returnvalue_node_more_loss_layer = self.structureparameter._get_electric_field_update_coefficients_h(
            self.structureparameter.loss_layer + 1)
        self.assertEquals(returnvalue_node_more_loss_layer,
                          Meshnodefield.updatecoefficient / self.structureparameter.relative_permittivity[
                              self.structureparameter.loss_layer + 1] / (
                              1.0 + self.structureparameter.loss))

    @patch.object(Structureparameter, '_get_magnetic_field_update_coefficients_h')
    @patch.object(Structureparameter, '_get_magnetic_field_update_coefficients_e')
    def test_set_magnetic_field_update_coefficients(self, mock_get_magnetic_field_update_coefficients_e,
                                                    mock_get_magnetic_field_update_coefficients_h):
        self.structureparameter._set_magnetic_field_update_coefficients()
        callcount_e = mock_get_magnetic_field_update_coefficients_e.call_count
        callcount_h = mock_get_magnetic_field_update_coefficients_h.call_count
        self.assertEqual(callcount_e, callcount_h)
        self.assertEqual(callcount_e, self.structureparameter.mesh_size)

    def test_get_magnetic_field_update_coefficients_e(self):
        result = self.structureparameter._get_magnetic_field_update_coefficients_e()
        self.assertEqual(result, 1.0 / Meshnodefield.updatecoefficient)

    def test_get_magnetic_field_update_coefficients_h(self):
        result = self.structureparameter._get_magnetic_field_update_coefficients_h()
        self.assertEqual(result, 1.0)
