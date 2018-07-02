#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt


def hypergeometric(list, b, r, k):
    list_hypergeometric = []
    for x in list:
        bx = math.factorial(b) / (math.factorial(x) * math.factorial(b-x))
        rkx = math.factorial(r) / (math.factorial(k-x) * math.factorial(r+x-k))
        brk = math.factorial(b+r) / (math.factorial(k) * math.factorial(b+r-k))
        px = float(bx)*rkx/brk
        list_hypergeometric.append(px)

    return list_hypergeometric


u = np.array([0,1,2,3])
t = hypergeometric(u, 4, 6, 3)

# plt.plot(u, t, 'bo')
plt.bar(u, t)
plt.axis([-1, 5, -0.75, 0.75])
plt.show()
