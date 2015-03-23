__author__ = 'yutongpang'
import numpy as np

from fdtdcode.fdtd_simulation import FDTDsimulation


fdtdsimulation = FDTDsimulation(200, 250)
fdtdsimulation.source.source_node = 50
fdtdsimulation.envole_field_with_time()

import matplotlib.pyplot as plt
x = np.arange(0, 200)
y = fdtdsimulation.electric_field_time[30, :]
plt.plot(x, y)
plt.show()