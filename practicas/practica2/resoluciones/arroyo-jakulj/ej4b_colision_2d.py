#!/usr/bin/python

import math
import random

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

Bordehor=100
Bordever=100
Bordehorneg=0
Bordeverneg=0

tgMatrix = [[0,1],[-1,0]]

# componentes de elementos
PX = 0
PY = 1
VX = 2
VY = 3
M = 4

class ParticleBox:    
    # columnas de init_state:
    #  0 posicion x
    #  1 posicion y
    #  2 velocidad x
    #  3 velocidad y
    #  4 M
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
        self.state[:, PX:PY+1] += dt * self.state[:, VX:VY+1]

        
        # check for crossing boundary
        crossed_x1 = (self.state[:, PX] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, PX] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, PY] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, PY] > self.bounds[3] - self.size)

        self.state[crossed_x1, VX] = abs(self.state[crossed_x1, VX])
        self.state[crossed_x2, VX] = -abs(self.state[crossed_x2, VX])
        self.state[crossed_y1, VY] = abs(self.state[crossed_y1, VY])
        self.state[crossed_y2, VY] = -abs(self.state[crossed_y2, VY])

        
        # check 2d collisions
        for i in range(0, len(self.state)):
            o1 = self.state[i]
            for j in range(i+1, len(self.state)):
                o2 = self.state[j]
                
                # cuando distancia(p1, p2) < r1 + r2
                diff = o1[PX:PY+1] - o2[PX:PY+1]
                dist = math.sqrt(diff[0] ** 2 + diff[1] ** 2)
        
                suma_de_radios = self.size + self.size
        
                if dist < suma_de_radios:
                    self.collision2d(o1, o2)

    def collision2d(self, o1, o2):
        # 1) normal and tangent direction
        p1 = o1[PX:PY+1]
        p2 = o2[PX:PY+1]

        n = p2 - p1
        if n[0] == 0 and n[1] == 0:
            n[0] = 1 # si estan en la misma posicion, dar una direccion default
        un = n / math.sqrt(n[0]**2 + n[1]**2)
        ut = np.zeros((2))
        ut[0] = -un[1]
        ut[1] = un[0]
        
        
        # 2) initial velocities
        v1 = o1[VX:VY+1].copy()
        v2 = o2[VX:VY+1].copy()
        
        
        # 3) velocities in normal and tangent direction
        v1n = v1.dot(un)
        v1t = v1.dot(ut)
        v2n = v2.dot(un)
        v2t = v2.dot(ut)
        
        
        # 4) new tangent velocities
        v1tf = v1t
        v2tf = v2t
        
        
        # 5) new normal velocities
        m1 = o1[M]
        m2 = o2[M]
        
        v1nf = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
        v2nf = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m2 + m1)
        
        
        # 6) new velocity vectors
        v1nfv = v1nf * un
        v1tfv = v1tf * ut
        v2nfv = v2nf * un
        v2tfv = v2tf * ut
        
        
        # 7) final velocities
        v1f = v1nfv + v1tfv
        v2f = v2nfv + v2tfv

        
        o1[VX:VY+1] = v1f
        o2[VX:VY+1] = v2f
        
        if False:
            print "Colisionaron en tiempo " + str(self.time_elapsed) + ":"
            print "  p1  = " + str(o1[PX:PY+1])
            print "  p2  = " + str(o2[PX:PY+1])
            print "  v1  = " + str(v1)
            print "  v2  = " + str(v2)
            print "  v1' = " + str(o1[VX:VY+1])
            print "  v2' = " + str(o2[VX:VY+1])



#------------------------------------------------------------

radio = 1.5

# set up initial state
cantidad = 50
min_vel = 40
max_vel = 80
r = random.random
w = Bordehor - Bordehorneg
h = Bordever - Bordeverneg
init_state = np.zeros((cantidad,5),dtype=float)
for i in range(0, cantidad):
    init_state[i, PX] = r() * w + Bordehorneg
    init_state[i, PY] = r() * h + Bordeverneg
    a = r() * 2 * math.pi                   # angulo de 0 a 2*math.pi
    v = r()**2 * (max_vel - min_vel) + min_vel  # velocidad de min_vel a max_vel
    init_state[i, VX] = math.cos(a) * v
    init_state[i, VY] = math.sin(a) * v
    init_state[i, M]  = 1

box = ParticleBox(init_state, size=radio)
dt = 1. / 240

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
    particles.set_markersize((radio*2)**2)
    return particles,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=20, interval=20, blit=True)

plt.show()
