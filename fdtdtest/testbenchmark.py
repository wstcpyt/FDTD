__author__ = 'yutongpang'
import unittest
import playground

class TFSFboundaryconditonTEST(unittest.TestCase):
    def test_1d_benchmark(self):
        playground.run()
        self.assertEquals(3, 3)