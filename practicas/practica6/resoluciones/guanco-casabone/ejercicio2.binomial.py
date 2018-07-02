#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt


def binomial(list, n, p):
    list_binomial = []
    for x in list:
        if x >= 0:
            px = math.factorial(len(list)) / (math.factorial(x)*math.factorial(n-x))
            list_binomial.append(px*(p**x)*((1-p)**(n-x)))
        else:
            list_binomial.append(0)

    return list_binomial


u = np.arange(20)
t = binomial(u, 20, 0.6)

plt.plot(u, t, 'bo')
plt.axis([-1, 20, -0.1, 0.7])
plt.show()
