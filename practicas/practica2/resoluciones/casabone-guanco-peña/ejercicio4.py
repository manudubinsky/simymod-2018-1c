#!/usr/bin/python
import numpy as np

from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import math

class ParticleBox:
    def __init__(self,
                 init_state=[[1, 0, 0, -1],
                             [-0.5, 0.5, 0.5, 0.5],
                             [-0.5, -0.5, -0.5, 0.5]],
                 bounds=[-50, 50, -50, 50],
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
        self.state[:, :2] += dt * self.state[:, 2:]

        d = math.sqrt((self.state[1, 0] - self.state[0, 0])**2 + (self.state[1, 1] - self.state[0, 1])**2)

        if (d) <= self.size:
            # 0- masas
            m1 = 1
            m2 = 1

            # 1- Busco el vector normal n, vector unitario un y vector tangente unitario ut
            n = np.array([self.state[1, 0] - self.state[0, 0], self.state[1, 1] - self.state[0, 1]])
            un = np.array([n[0]/np.linalg.norm(n), n[1]/np.linalg.norm(n)])
            ut = np.array([-un[1], un[0]])

            # 2- Velocidades actuales
            v1 = np.array([self.state[0, 2], self.state[0, 3]])
            v2 = np.array([self.state[1, 2], self.state[1, 3]])

            # 3- Actualizo velocidades
            v1n = np.dot(un, v1)
            v1t = np.dot(ut, v1)
            v2n = np.dot(un, v2)
            v2t = np.dot(ut, v2)

            # 4- Busco las nuevas velocidades tangenciales
            v1pt = v1t
            v2pt = v2t

            # 5- Busco las velocidades normales
            v1pn = (v1n*(m1 - m2) + 2*m2*v2n) / (m1 + m2)
            v2pn = (v2n*(m2 - m1) + 2*m1*v1n) / (m1 + m2)

            # 6- Convertir los escalares y las velocidades tangenciales en vectores
            v1pn = v1pn * un
            v1pt = v1pt * ut
            v2pn = v2pn * un
            v2pt = v2pt * ut

            # 7- Busco las velocidades finales
            v1p = v1pn + v1pt
            v2p = v2pn + v2pt

            # 8- Actualizo las velocidades finales
            self.state[0, 2] = v1p[0]
            self.state[0, 3] = v1p[1]
            self.state[1, 2] = v2p[0]
            self.state[1, 3] = v2p[1]

        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

        self.state[crossed_x1 | crossed_x2, 2] *= 0
        self.state[crossed_y1 | crossed_y2, 3] *= 0


# ------------------------------------------------------------
# set up initial state
init_state = np.zeros((2, 4), dtype=float)
init_state[0, 0] = -20
init_state[0, 1] = 1
init_state[0, 2] = 10
init_state[0, 3] = 0

init_state[1, 0] = 10
init_state[1, 1] = 0
init_state[1, 2] = 0
init_state[1, 3] = 0

box = ParticleBox(init_state, size=2.5)
dt = 1. / 30  # 30fps

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
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
