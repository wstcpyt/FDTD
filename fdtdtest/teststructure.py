__author__ = 'yutongpang'
import unittest
import numpy as np
from unittest.mock import patch
from fdtdcode.structure import Structureparameter
from fdtdcode.field import Meshnodefield


class PermittivityTEST(unittest.TestCase):
    def setUp(self):
        self.structureparameter = Structureparameter(100)

    @patch.object(Structureparameter, '_set_lossy_matrial_update_coefficient_magnetic')
    @patch.object(Structureparameter, '_set_lossy_matrial_update_coefficient_electric')
    @patch.object(Structureparameter, '_set_relative_permittivity')
    def test_init_structure_permittivity(self, mock_set_relative_permittivity,
                                         mock_set_lossy_matrial_update_coefficient_electric,
                                         mock_set_lossy_matrial_update_coefficient_magnetic):
        self.structureparameter = Structureparameter(100)
        mock_set_relative_permittivity.return_value = np.ones(self.structureparameter.mesh_size)
        mock_set_relative_permittivity.assert_called_once_with()
        mock_set_lossy_matrial_update_coefficient_electric.assert_called_once_with()
        mock_set_lossy_matrial_update_coefficient_magnetic.assert_called_once_with()

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

    @patch.object(Structureparameter, '_get_lossy_matrial_update_coefficient_electric')
    def test_set_lossy_matrial_update_coefficient_electric(self, mock_get_lossy_matrial_update_coefficient_electric):
        returnvalue = self.structureparameter._set_lossy_matrial_update_coefficient_electric()
        length = len(returnvalue)
        self.assertEquals(length, self.structureparameter.mesh_size)
        callcount = mock_get_lossy_matrial_update_coefficient_electric.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_lossy_matrial_update_coefficient_electric(self):
        returnvalue_node_less_100 = self.structureparameter._get_lossy_matrial_update_coefficient_electric(50)
        self.assertEquals(returnvalue_node_less_100, 1.0)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_lossy_matrial_update_coefficient_electric(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          (1.0 - self.structureparameter.loss)/(1.0 + self.structureparameter.loss))

    @patch.object(Structureparameter, '_get_lossy_matrial_update_coefficient_magnetic')
    def test_set_lossy_matrial_update_coefficient_electric(self, mock_get_lossy_matrial_update_coefficient_magnetic):
        returnvalue = self.structureparameter._set_lossy_matrial_update_coefficient_magnetic()
        length = len(returnvalue)
        self.assertEquals(length, self.structureparameter.mesh_size)
        callcount = mock_get_lossy_matrial_update_coefficient_magnetic.call_count
        self.assertEquals(callcount, self.structureparameter.mesh_size)

    def test_get_lossy_matrial_update_coefficient_magnetic(self):
        returnvalue_node_less_100 = self.structureparameter._get_lossy_matrial_update_coefficient_magnetic(50)
        self.assertEquals(returnvalue_node_less_100, Meshnodefield.updatecoefficient)
        returnvalue_node_equal_or_more_100 = self.structureparameter._get_lossy_matrial_update_coefficient_magnetic(150)
        self.assertEquals(returnvalue_node_equal_or_more_100,
                          Meshnodefield.updatecoefficient/9.0/(1.0+self.structureparameter.loss))