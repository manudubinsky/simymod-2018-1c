#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math

# constantes
w = math.pi
orbita = 10
radio = 1

intervalo = 20
dt = 0.001 * intervalo

# globales
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-15, 15), ylim=(-15, 15))
patch = plt.Circle((0,0), radius = radio, fc='y')

tiempo_transcurrido = 0

def init():
	patch.center = (0,0)
	ax.add_patch(patch)
	return patch,

def animate(i):
	global tiempo_transcurrido, orbita, w
	tiempo_transcurrido += dt
	x, y = patch.center
	
	
	angulo = w * tiempo_transcurrido
	x = math.cos(angulo) * orbita
	y = math.sin(angulo) * orbita
	
	
	patch.center = (x, y)
	print i
	return patch,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360,
                               interval=intervalo,
                               blit=True)

plt.show()
