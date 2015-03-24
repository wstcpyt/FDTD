__author__ = 'yutongpang'
import unittest
from fdtdcode.structure import Permittivity


class PermittivityTEST(unittest.TestCase):
    def test_init_structure_permittivity(self):
        permittivity = Permittivity(100)
        size = len(permittivity.relative_permittivity)
        self.assertEquals(size, 100)
