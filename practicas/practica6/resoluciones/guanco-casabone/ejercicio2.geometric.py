#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt


def geometric(list, p):
    list_geometric = []
    for x in list:
        if x > 0:
            list_geometric.append(p*(1-p)**(x-1))
        else:
            list_geometric.append(0)

    return list_geometric


u = np.arange(20)
t = geometric(u, 0.3)

plt.plot(u, t, 'bo')
plt.axis([-1, 20, -0.1, 0.4])
plt.show()
