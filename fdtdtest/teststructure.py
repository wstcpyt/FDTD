__author__ = 'yutongpang'
import unittest
import numpy as np
from unittest.mock import patch
from fdtdcode.structure import Permittivity


class PermittivityTEST(unittest.TestCase):
    def setUp(self):
        self.permittivity = Permittivity(100)

    @patch.object(Permittivity, '_set_relative_permittivity')
    def test_init_structure_permittivity(self, mock_set_relative_permittivity):
        self.permittivity = Permittivity(100)
        mock_set_relative_permittivity.return_value = np.ones(self.permittivity.mesh_size)
        mock_set_relative_permittivity.assert_called_once_with()

    @patch.object(Permittivity, '_get_relative_permittivity_in_single_node')
    def test_set_relative_permittivity(self, mock_get_relative_permittivity_in_single_node):
        returnvalue = self.permittivity._set_relative_permittivity()
        length = len(returnvalue)
        self.assertEquals(length, self.permittivity.mesh_size)
        callcount = mock_get_relative_permittivity_in_single_node.call_count
        self.assertEquals(callcount, self.permittivity.mesh_size)

    def test_get_relative_permittivity_in_single_node(self):
        returnvalue_node_less_100 = self.permittivity._get_relative_permittivity_in_single_node(50)
        self.assertEquals(returnvalue_node_less_100, 1)
        returnvalue_node_equal_or_more_100 = self.permittivity._get_relative_permittivity_in_single_node(150)
        self.assertEquals(returnvalue_node_equal_or_more_100, 9)
