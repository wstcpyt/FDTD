__author__ = 'yutongpang'
import numpy as np
from fdtdcode.fdtd_simulation import FDTDsimulation

def run():
    fdtdsimulation = FDTDsimulation(200, 450)
    fdtdsimulation.tfsfboundarycondition.magnetic_tfsf_node_index = 49
    fdtdsimulation.envole_field_with_time()