#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt


def inverse_transform(list, lambda1):
    list_x = []
    for u in list:
        x = -1.0*(math.log(1-u,math.e)/lambda1)
        list_x.append(x)

    return list_x


u = np.random.rand(10000)
x = inverse_transform(u, 2)

plt.plot(x, u, 'bo')
plt.show()
