#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)
u=[]
t=[]
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Circle((5, -5), 2, fc='r')

def cooling(T0, k, T_s, t_end, dt, theta=0.5):
    global u, t 
    dt = float(dt)
    Nt = int(round(t_end/dt))
    T = Nt*dt
    u = np.zeros(Nt+1)
    t = np.linspace(0, t_end, Nt+1)
    u[0] = T0
    for n in range(0, t_end):
        u[n+1] = (u[n] + dt*(theta*-k*T_s + (1.0 - theta)*(-k*u[n] + k*T_s)))/(1.0 + k*theta*dt)
    return u, t

def init():
    global u, t 
    patch.center = (5, 5)
    u, t = cooling(37, 0.134, 20, 30, 1, 0)
    print u, t
    ax.add_patch(patch)
    return patch,

def animate(i):
    global u, t    
    x, y = patch.center
    patch.center = (x, y)
    a = float(u[i])/100
    patch.set_facecolor(colors.ColorConverter.to_rgba('blue', alpha=a))
   
    return patch,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=31,
                               interval=20,
                               blit=True)

plt.show()
