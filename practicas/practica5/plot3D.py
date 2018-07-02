import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


n = 2.*np.pi
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(0,n,100)
y = np.linspace(0,n,100)
x,y = np.meshgrid(x,y)
z = np.sin(x+y)
line = ax.plot_surface(x, y, z,color= 'b')

plt.show()
