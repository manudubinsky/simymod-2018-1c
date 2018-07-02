#!/usr/bin/python

import math

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

Bordehor=50
Bordever=50
Bordehorneg=-50
Bordeverneg=-50

def abs(x):
    if x < 0:
        return -x
    else:
        return x

class ParticleBox:
    # columnas de init_state:
    #  0 posicion x
    #  1 posicion y
    #  2 velocidad x
    #  3 velocidad y
    #  4 masa
    def __init__(self,
                 init_state,
                 bounds = [Bordehorneg, Bordehor, Bordeverneg, Bordever],
                 size = 1.25):
        self.init_state = np.asarray(init_state, dtype=float)
        self.size = size
        self.state = self.init_state.copy()
        self.time_elapsed = 0
        self.bounds = bounds
        self.colisiono = False

    def step(self, dt):
        """step once by dt seconds"""
        self.time_elapsed += dt

        # update positions
        self.state[:, 0:2] += dt * self.state[:, 2:4]
        
        # check for crossing boundary
        #crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)

        # self.state[crossed_x1 | crossed_x2, 2] *= 
        #self.state[crossed_y1, 1] = self.bounds[2] + self.size
        
        # verificar si colisionan
        # distancia(p1, p2) < r1 + r2
        distancia = abs(self.state[0, 0] - self.state[1, 0])
        
        suma_de_radios = self.size + self.size
        
        if distancia < suma_de_radios:
            m1 = self.state[0, 4]
            m2 = self.state[1, 4]

            vi1 = self.state[0, 2]
            vi2 = self.state[1, 2]

            vf1 = ((m1-m2) / (m1+m2)) * vi1 + ((2*m2) / (m1+m2)) * vi2
            vf2 = ((m2-m1) / (m2+m1)) * vi2 + ((2*m1) / (m2+m1)) * vi1

            self.state[0, 2] = vf1
            self.state[1, 2] = vf2
            
            print "Colisionaron en tiempo " + str(self.time_elapsed) + ":"
            print "  x1 = " + str(self.state[0, 0])
            print "  x2 = " + str(self.state[1, 0])
            print "  vi1 = " + str(vi1)
            print "  vi2 = " + str(vi2)
            print "  vf1 = " + str(vf1)
            print "  vf2 = " + str(vf2)


#------------------------------------------------------------

radio = 1.25
xi1 = -20
xi2 = 20
vi1 = 20
vi2 = 1
m1 = 1000
m2 = 1

# set up initial state
init_state = np.zeros((2,5),dtype=float)

init_state[0, 0] = xi1
init_state[0, 1] = 0
init_state[0, 2] = vi1
init_state[0, 3] = 0
init_state[0, 4] = m1

init_state[1, 0] = xi2
init_state[1, 1] = 0
init_state[1, 2] = vi2
init_state[1, 3] = 0
init_state[1, 4] = m2


box = ParticleBox(init_state, size=radio)
dt = 1. / 30

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(Bordehorneg, Bordehor), ylim=(Bordeverneg, Bordever))
particles, = ax.plot([], [], 'bo', ms=radio*2)

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
    particles.set_markersize(radio*2)
    return particles,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
