import numpy as np
import matplotlib.pyplot as plt

def u(t):
    return np.sin(t) + np.cos(t)

t = np.arange(0.0, 4*np.pi, 0.01)

plt.plot(t, u(t), 'b')
plt.show()
