#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt


def pascal(list, m, p):
    list_pascal = []
    for k in list:
        if k >= m:
            px = math.factorial(k - 1) / (math.factorial(m - 1) * (math.factorial(k - m)))
            list_pascal.append(px*(p**m)*((1-p)**(k-m)))
        else:
            list_pascal.append(0)

    return list_pascal


u = np.arange(20)
t = pascal(u, 3, 0.5)

plt.plot(u, t, 'bo')
plt.axis([-1, 20, -0.1, 0.2])
plt.show()
