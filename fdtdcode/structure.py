__author__ = 'yutongpang'
import numpy as np


class Permittivity():
    def __init__(self, mesh_size):
        self.mesh_size = mesh_size
        self.relative_permittivity = self._set_relative_permittivity()

    def _set_relative_permittivity(self):
        relative_permittivity = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            relative_permittivity[field_node_index] = self._get_relative_permittivity_in_single_node(field_node_index)
        return relative_permittivity

    @staticmethod
    def _get_relative_permittivity_in_single_node(field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return 9.0