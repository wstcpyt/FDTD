__author__ = 'yutongpang'
import numpy as np
from fdtdcode.field import Meshnodefield


class Structureparameter():
    def __init__(self, mesh_size):
        self.mesh_size = mesh_size
        self.loss = 0.01
        self.relative_permittivity = self._set_relative_permittivity()
        self.lossy_matrial_update_coefficient_electric = self._set_lossy_matrial_update_coefficient_electric()
        self.lossy_matrial_update_coefficient_magnetic = self._set_lossy_matrial_update_coefficient_magnetic()

    def _set_relative_permittivity(self):
        relative_permittivity = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            relative_permittivity[field_node_index] = self._get_relative_permittivity_in_single_node(field_node_index)
        return relative_permittivity

    def _set_lossy_matrial_update_coefficient_electric(self):
        lossy_matrial_update_coefficient_electric = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            lossy_matrial_update_coefficient_electric[field_node_index] \
                = self._get_lossy_matrial_update_coefficient_electric(field_node_index)
        return lossy_matrial_update_coefficient_electric

    def _set_lossy_matrial_update_coefficient_magnetic(self):
        lossy_matrial_update_coefficient_magnetic = np.zeros(self.mesh_size)
        for field_node_index in range(self.mesh_size):
            lossy_matrial_update_coefficient_magnetic[field_node_index] \
                = self._get_lossy_matrial_update_coefficient_magnetic(field_node_index)
        return lossy_matrial_update_coefficient_magnetic

    def _get_lossy_matrial_update_coefficient_magnetic(self, field_node_index):
        if field_node_index < 100:
            return Meshnodefield.updatecoefficient
        else:
            return Meshnodefield.updatecoefficient/9.0/(1.0 + self.loss)

    def _get_lossy_matrial_update_coefficient_electric(self, field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return (1.0 - self.loss)/(1.0 + self.loss)

    @staticmethod
    def _get_relative_permittivity_in_single_node(field_node_index):
        if field_node_index < 100:
            return 1.0
        else:
            return 9.0