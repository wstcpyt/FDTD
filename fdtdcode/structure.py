__author__ = 'yutongpang'
import numpy as np


class Permittivity():
    def __init__(self, mash_size):
        self.relative_permittivity = np.ones(mash_size)