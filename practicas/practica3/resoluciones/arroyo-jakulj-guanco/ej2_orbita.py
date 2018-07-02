#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math

# constantes
w = math.pi
orbita = 5
radio0 = 1
radio1 = 0.5

intervalo = 20
dt = 0.001 * intervalo

# globales
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
centro = plt.Circle((0,0), radius = radio0, fc='y')
satelite = plt.Circle((0,0), radius = radio1, fc='b')

tiempo_transcurrido = 0

def init():
	centro.center = (2,2)
	satelite.center = (0,0)
	ax.add_patch(centro)
	ax.add_patch(satelite)
	return satelite,

def animate(i):
	global tiempo_transcurrido, orbita, w
	tiempo_transcurrido += dt
	
	# centro
	cx, cy = centro.center
	
	# satelite
	x, y = satelite.center
	angulo = w * tiempo_transcurrido
	x = math.cos(angulo) * orbita + cx
	y = math.sin(angulo) * orbita + cy
	satelite.center = (x, y)
	
	return satelite,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360,
                               interval=intervalo,
                               blit=True)

plt.show()
