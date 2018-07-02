import numpy as np
import matplotlib.pyplot as plt

def u(t):
    return np.sin(t) + np.cos(t)

def uPlus(t,h):
    return (np.sin(t + h) + np.cos(t + h) - (np.sin(t) + np.cos(t)))/h

t = np.arange(0., 4.*np.pi, 0.1)

plt.plot(t, u(t), 'b')
plt.plot(t, uPlus(t,0.5), 'r')
plt.show()
