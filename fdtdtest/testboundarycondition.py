__author__ = 'yutongpang'
import sys

sys.path.append('/Users/yutongpang/PycharmProjects/FDTD')
import unittest
from unittest.mock import patch
from fdtdcode.boundaryconditon import TFSFboundarycondition
from math import exp
from fdtdcode.field import Meshnodefield


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

    def test_get_magnetic_source_correction(self):
        returnvalue = self.tfsfboundarycondition._get_magnetic_source_correction(1)
        self.assertEqual(returnvalue, exp(-(1 - 30.0) ** 2 / 100.0) / Meshnodefield.updatecoefficient)

    def test_get_electric_source_correction(self):
        returnvalue = self.tfsfboundarycondition._get_electric_source_correction(1)
        self.assertEqual(returnvalue, exp(-(1 - 30.0 + 1) ** 2 / 100.0))