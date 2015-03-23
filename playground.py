__author__ = 'yutongpang'
from fdtd_simulation import FDTDsimulation
import numpy as np

fdtdsimulation = FDTDsimulation(200, 250)
fdtdsimulation.envole_field_with_time()

import matplotlib.pyplot as plt
x = np.arange(0, 200)
y = fdtdsimulation.electric_field_time[40, :]
plt.plot(x, y)
plt.show()