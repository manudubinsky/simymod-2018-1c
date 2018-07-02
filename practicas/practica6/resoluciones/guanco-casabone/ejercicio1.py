#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt

# list = np.random.rand(100)
# list = np.random.rand(1000)
# list = np.random.rand(1000)
list = np.random.rand(100000)

plt.hist(list, 50)
plt.show()
