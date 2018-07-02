#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math

# constantes

radioParticula = 1

radioDesdeEje = 10


velocidadAngular = (2 * math.pi) / 5


limite = 12

intervalo = 20
dt = 0.001 * intervalo

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-limite, limite), ylim=(-limite, limite))
particle = plt.Circle((0,0), radius = radioParticula, fc=(0.25,0.25,0.25))

ax.axhline(linewidth=0.4, color="black")
ax.axvline(linewidth=0.4, color="black")
ax.grid(color='r', linestyle='-', linewidth=0.2)



tiempo_transcurrido = 0

def init():
	particle.center = (0,0)
	ax.add_patch(particle)
	return particle,

def animate(i):
	global tiempo_transcurrido, radioDesdeEje
	tiempo_transcurrido += dt
	
	# particle
	mx, my = particle.center
	angulo = velocidadAngular * tiempo_transcurrido
	mx = math.cos(angulo) * radioDesdeEje 
	my = math.sin(angulo) * radioDesdeEje 
	particle.center = (mx, my)
	
	return particle,

anim = animation.FuncAnimation(fig, animate, 
							   init_func=init, 
							   frames=360,
							   interval=intervalo,
							   blit=True)

							   

plt.show()
