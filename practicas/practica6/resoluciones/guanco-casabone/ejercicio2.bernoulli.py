#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt


def bernoulli(list, p):
    list_bernoulli = []
    for x in list:
        if x == 1:
            list_bernoulli.append(p)
        elif x == 0:
            list_bernoulli.append(1-p)
        else:
            list_bernoulli.append(0)

    return list_bernoulli


u = np.arange(10)
t = bernoulli(u, 0.3)

plt.plot(u, t, 'bo')
plt.axis([-1,10,-1,1])
plt.show()
