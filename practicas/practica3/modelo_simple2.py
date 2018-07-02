#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Circle((5, -5), 0.2, fc='y')

def init():
	patch.center = (5, 5)
	ax.add_patch(patch)
	return patch,

def animate(i):
	x, y = patch.center
	x = 0.01 * i
	y = 0.01 * i
	patch.center = (x, y)
	return patch,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
