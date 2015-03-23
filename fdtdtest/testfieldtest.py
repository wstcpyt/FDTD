__author__ = 'yutongpang'
import unittest
from unittest.mock import patch

import numpy as np
import numpy.testing as npt

from fdtdcode.field import Meshnodefield, Singlenodefield


class MeshnodefieldTest(unittest.TestCase):
    def setUp(self):
        self.meshnodefield = Meshnodefield(2)

    @patch.object(Singlenodefield, 'update_magnetic_field')
    def test_update_magnetic_field_mesh(self, mock_update_magnetic_field):
        self.__initiate_meshnodefield_variable()
        mock_update_magnetic_field.return_value = 2.0
        expectedresult = self.meshnodefield.update_magnetic_field_mesh()
        npt.assert_array_equal(expectedresult, np.array([2.0, 2.0, 3.0]))

    @patch.object(Singlenodefield, 'update_electric_field')
    def test_update_electric_field_mesh(self, mock_update_electric_field):
        self.__initiate_meshnodefield_variable()
        mock_update_electric_field.return_value = 2.0
        expectedresult = self.meshnodefield.update_electric_field_mesh()
        npt.assert_array_equal(expectedresult, np.array([1.0, 2.0, 2.0]))

    def test_meshnodefield_can_init_mesh_size(self):
        self.assertEqual(self.meshnodefield.mesh_size, 2)

    def __initiate_meshnodefield_variable(self):
        self.meshnodefield.magnetic_field_y = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.electric_field_z = np.array([1.0, 2.0, 3.0])
        self.meshnodefield.mesh_size = len(self.meshnodefield.electric_field_z)


class SinglenodefieldTEST(unittest.TestCase):
    def setUp(self):
        self.singlenodefiled = Singlenodefield()
        self.updatingcoeffiecient = self.singlenodefiled.updatecoefficient

    def test_update_magnetic_field(self):
        expectedresult = self.singlenodefiled.update_magnetic_field(0, 0, 1)
        self.assertEqual(expectedresult, 1/self.updatingcoeffiecient)

    def test_update_electric_field(self):
        expectedresult = self.singlenodefiled.update_electric_field(0, 0, 1)
        self.assertEqual(expectedresult, 1*self.updatingcoeffiecient)