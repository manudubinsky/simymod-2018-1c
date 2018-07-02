#!/usr/bin/python

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


class ParticleBox:
    def __init__(self,
                 init_state=[[1, 0, 0, -1],
                             [-0.5, 0.5, 0.5, 0.5],
                             [-0.5, -0.5, -0.5, 0.5]],
                 bounds=[0, 800, 0, 600],
                 size=0.04):
        self.init_state = np.asarray(init_state, dtype=float)
        self.size = size
        self.state = self.init_state.copy()
        self.time_elapsed = 0
        self.bounds = bounds

    def step(self, dt):
        """step once by dt seconds"""
        self.time_elapsed += dt

        # update positions
        self.state[:, 3] += -9.91*dt
        self.state[:, 1] += self.state[:, 3]*dt - 0.5*9.91*(dt**2)
        self.state[:, 0] += dt * self.state[:, 2]

        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

        self.state[crossed_x1 | crossed_x2, 0] = self.size
        self.state[crossed_y1 | crossed_y2, 1] = self.size
        self.state[crossed_x1 | crossed_x2, 2] = 0
        self.state[crossed_y1 | crossed_y2, 3] = 0

        if crossed_y1:
            print self.time_elapsed


# ------------------------------------------------------------
# set up initial state
init_state = np.zeros((1, 4), dtype=float)
init_state[0, 0] = 0
init_state[0, 1] = 50
init_state[0, 2] = 30.85
init_state[0, 3] = 100

box = ParticleBox(init_state, size=0)
dt = 1. / 30  # 30fps

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 800), ylim=(0, 600))
particles, = ax.plot([], [], 'bo', ms=5)


# initialization function: plot the background of each frame
def init():
    global box
    particles.set_data([], [])
    return particles,


# animation function.  This is called sequentially
def animate(i):
    global box, dt, ax, fig
    box.step(dt)

    particles.set_data(box.state[:, 0], box.state[:, 1])
    particles.set_markersize(5)
    return particles,


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
