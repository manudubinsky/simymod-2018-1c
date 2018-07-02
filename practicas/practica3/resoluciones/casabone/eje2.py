#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math

# constantes

radioParticula = 1

radioDesdeEje = 5


velocidadAngular = (2 * math.pi) / 5


limite = 8

intervalo = 20
dt = 0.001 * intervalo

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-limite, limite), ylim=(-limite, limite))
particle1 = plt.Circle((0,0), radius = radioParticula, fc=(0.25,0.25,0.25))
particle2 = plt.Circle((0,0), radius = radioParticula, fc=(0.25,0.25,0.25))

ax.axhline(linewidth=0.4, color="black")
ax.axvline(linewidth=0.4, color="black")
ax.grid(color='r', linestyle='-', linewidth=0.2)



tiempo_transcurrido = 0

def init():
	particle1.center = (0,0)
	particle2.center = (2,2)
	ax.add_patch(particle1)	
	ax.add_patch(particle2)
	return particle1, particle2,

def animate(i):
	global tiempo_transcurrido, radioDesdeEje
	tiempo_transcurrido += dt
	
	cx, cy = particle2.center
	print(particle2.center)
	# particle
	mx, my = particle1.center
	angulo = velocidadAngular * tiempo_transcurrido
	mx = math.cos(angulo) * radioDesdeEje + cx
	my = math.sin(angulo) * radioDesdeEje + cy
	particle1.center = (mx, my)
	
	return particle1, particle2

anim = animation.FuncAnimation(fig, animate, 
							   init_func=init, 
							   frames=360,
							   interval=intervalo,
							   blit=True)

							   

plt.show()
