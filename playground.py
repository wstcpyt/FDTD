__author__ = 'yutongpang'
import numpy as np

from fdtdcode.fdtd_simulation import FDTDsimulation


fdtdsimulation = FDTDsimulation(200, 450)
fdtdsimulation.source.source_node = 50
fdtdsimulation.envole_field_with_time()

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
plt.imshow(fdtdsimulation.electric_field_time)
plt.show()