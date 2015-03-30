__author__ = 'yutongpang'
import sys

sys.path.append('/Users/yutongpang/PycharmProjects/FDTD')
import unittest
from unittest.mock import patch
from fdtdcode.boundaryconditon import TFSFboundarycondition
from fdtdcode.source import Source


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
        mock_get_additive_source_function_at_time_node_index.assert_called_once_with(1+0.5, -0.5)