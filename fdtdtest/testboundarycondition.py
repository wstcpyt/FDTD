__author__ = 'yutongpang'
import sys

sys.path.append('/Users/yutongpang/PycharmProjects/FDTD')
import unittest
from unittest.mock import patch
from fdtdcode.boundaryconditon import TFSFboundarycondition
from fdtdcode.source import Source
from fdtdcode.boundaryconditon import Absorption
import numpy as np


class TFSFboundaryconditonTEST(unittest.TestCase):
    def setUp(self):
        self.tfsfboundarycondition = TFSFboundarycondition(1)

    def test_tfsfboundarycondition_can_set_magnetic_tfsf_node_index(self):
        result = self.tfsfboundarycondition.magnetic_tfsf_node_index
        self.assertEquals(result, 1)

    @patch.object(TFSFboundarycondition, '_get_electric_source_correction')
    @patch.object(TFSFboundarycondition, '_get_magnetic_source_correction')
    def test_incidence_source_correction_function(self, mock_magnetic_source_function, mock_electric_source_function):
        self.tfsfboundarycondition.get_incidence_source_correction(0, 0)
        mock_magnetic_source_function.assert_called_once_with(0)
        self.tfsfboundarycondition.get_incidence_source_correction(0, 1)
        mock_electric_source_function.assert_called_once_with(0)

    @patch.object(Source, 'get_additive_source_function_at_time_node_index')
    def test_get_magnetic_source_correction(self, mock_get_additive_source_function_at_time_node_index):
        mock_get_additive_source_function_at_time_node_index.return_value = 1.0
        self.tfsfboundarycondition._get_magnetic_source_correction(1)
        mock_get_additive_source_function_at_time_node_index.assert_called_once_with(1, 0)

    @patch.object(Source, 'get_additive_source_function_at_time_node_index')
    def test_get_electric_source_correction(self, mock_get_additive_source_function_at_time_node_index):
        mock_get_additive_source_function_at_time_node_index.return_value = 1.0
        self.tfsfboundarycondition._get_electric_source_correction(1)
        mock_get_additive_source_function_at_time_node_index.assert_called_once_with(1 + 0.5, -0.5)


class AbsorptionTEST(unittest.TestCase):
    def setUp(self):
        self.absorption = Absorption(100, np.zeros(100), np.zeros(100))

    @patch.object(Absorption, '_set_absorption_rightend_coefficient')
    @patch.object(Absorption, '_init_constant_and_variable')
    @patch.object(Absorption, '_set_absorption_leftend_coefficient')
    def test_init_absorption(self, mock__set_absorption_leftend_coefficient,
                             mock_init_constant_and_variable,
                             mock_set_absorption_rightend_coefficient):
        Absorption(100, 1, 1)
        mock__set_absorption_leftend_coefficient.assert_called_once_with()
        mock_set_absorption_rightend_coefficient.assert_called_once_with()
        mock_init_constant_and_variable.assert_called_once_with(100, 1, 1)

    def test_init_constant_and_variable(self):
        self.assertEquals(self.absorption.mesh_size, 100)
        self.assertEquals(len(self.absorption.electric_field_update_coefficients_h), 100)
        self.assertEquals(len(self.absorption.magnetic_field_update_coefficients_e), 100)
        self.assertEquals(self.absorption.electric_old_left, 0)
        self.assertEquals(self.absorption.electric_old_right, 0)

    @patch.object(Absorption, '_get_absorption_leftend_coefficient')
    def test_set_absorption_leftend_coefficient(self, mock_get_absorption_leftend_coefficient):
        mock_get_absorption_leftend_coefficient.return_value = 2.0
        self.absorption._set_absorption_leftend_coefficient()
        mock_get_absorption_leftend_coefficient.assert_called_once_with()
        self.assertEquals(self.absorption.absorption_leftend_coefficient, 2.0)

    def test_get_absorption_leftend_coefficient(self):
        self.absorption.electric_field_update_coefficients_h[0] = 1
        self.absorption.magnetic_field_update_coefficients_e[0] = 1
        return_value = self.absorption._get_absorption_leftend_coefficient()
        self.assertEquals(return_value, 0)

    @patch.object(Absorption, '_get_absorption_rightend_coefficient')
    def test_set_absorption_rightend_coefficient(self, mock_get_absorption_rightend_coefficient):
        mock_get_absorption_rightend_coefficient.return_value = 2.0
        self.absorption._set_absorption_rightend_coefficient()
        mock_get_absorption_rightend_coefficient.assert_called_once_with()
        self.assertEquals(self.absorption.absorption_rightend_coefficient, 2.0)

    def test_get_absorption_rightend_coefficient(self):
        self.absorption.electric_field_update_coefficients_h[99] = 1
        self.absorption.magnetic_field_update_coefficients_e[98] = 1
        return_value = self.absorption._get_absorption_rightend_coefficient()
        self.assertEquals(return_value, 0)

    @patch.object(Absorption, '_set_electric_old_left')
    def test_get_electric_field_at_left_end(self, mock_set_electric_old_left):
        result = self.absorption.get_electric_field_at_left_end(1, 1)
        mock_set_electric_old_left.assert_called_once_with(1)
        self.assertEquals(result, 0)

    def test_set_electric_old_left(self):
        self.absorption._set_electric_old_left(2)
        self.assertEquals(self.absorption.electric_old_left, 2)

    @patch.object(Absorption, '_set_electric_old_right')
    def test_get_electric_field_at_right_end(self, mock_set_electric_old_right):
        result = self.absorption.get_electric_field_at_right_end(1, 1)
        mock_set_electric_old_right.assert_called_once_with(1)
        self.assertEquals(result, 0)

    def test_set_electric_old_right(self):
        self.absorption._set_electric_old_right(2)
        self.assertEquals(self.absorption.electric_old_right, 2)