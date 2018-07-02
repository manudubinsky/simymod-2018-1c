import numpy as np
import matplotlib.pyplot as plt
import math as m

def u(x):
    return m.sin(x) + m.cos(x)

h = 0.01

x = np.arange(-4*m.pi, 4*m.pi, h)
y = np.vectorize(u)(x)

plt.plot(x, y)
plt.ylabel('u(x)')
plt.show()
