#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt


def box_muller(u, v):
    X = []
    Y = []
    for x in range(0, len(u)):
        U = u[x]
        V = v[x]
        X.append(math.sqrt(-2*math.log(U))*math.cos(2*math.pi*V))
        Y.append(math.sqrt(-2*math.log(U))*math.sin(2*math.pi*V))

    return X,Y


u = np.random.rand(10000)
v = np.random.rand(10000)
x,y = box_muller(u, v)

plt.plot(x, y, 'bo')
plt.show()
