__author__ = 'yutongpang'

from fdtdcode.fdtd_simulation import FDTDsimulation


fdtdsimulation = FDTDsimulation(200, 450)
fdtdsimulation.tfsfboundarycondition.magnetic_tfsf_node_index = 49
fdtdsimulation.envole_field_with_time()

import matplotlib.pyplot as plt
plt.imshow(fdtdsimulation.electric_field_time)
plt.show()