#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math


tmes = 4
tdia = tmes / 30.0
tanio = 12.0 * tmes

radioParticulaSol = 140000 
radioParticulaTierra = 64000
radioParticulaLuna = 18000 

#Distancia de la tierra al sol (no son las reales)
radioDesdeEjeTierra = 1000000
radioDesdeEjeLuna = 100000

#Velocidad angular de TIerra y Luna
VelocidadAngularTierra = (2 * math.pi) / tanio
VelocidadAngularLuna = (2 * math.pi) / tmes

limite = 1300000

intervalo = 20
dt = 0.001 * intervalo

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-limite, limite), ylim=(-limite, limite))

Sol = plt.Circle((0,0), radius = radioParticulaSol, fc=(0.25,0.25,0.25))
Tierra = plt.Circle((0,0), radius = radioParticulaTierra, fc=(0.25,0.25,0.25))
Luna = plt.Circle((0,0), radius = radioParticulaLuna, fc=(0.25,0.25,0.25))

ax.axhline(linewidth=0.4, color="black")
ax.axvline(linewidth=0.4, color="black")
ax.grid(color='r', linestyle='-', linewidth=0.2)



tiempo_transcurrido = 0

def init():
	Sol.center = (0,0)
	Tierra.center = (0,0)
	Luna.center = (0,0)
	ax.add_patch(Sol)	
	ax.add_patch(Tierra)
	ax.add_patch(Luna)
	return Sol, Tierra, Luna,

def animate(i):
	global tiempo_transcurrido, radioDesdeEjeTierra, radioDesdeEjeLuna
	tiempo_transcurrido += dt
		
	sx, sy = Sol.center
	
	tx, ty = Tierra.center
	angulo = VelocidadAngularTierra * tiempo_transcurrido
	tx = math.cos(angulo) * radioDesdeEjeTierra + sx
	ty = math.sin(angulo) * radioDesdeEjeTierra + sy
	Tierra.center = (tx, ty)
		
	lx, ly = Luna.center
	angulo = VelocidadAngularLuna * tiempo_transcurrido
	lx = math.cos(angulo) * radioDesdeEjeLuna + tx
	ly = math.sin(angulo) * radioDesdeEjeLuna + ty
	Luna.center = (lx, ly)	
	
	return Sol, Tierra, Luna,

anim = animation.FuncAnimation(fig, animate, 
							   init_func=init, 
							   frames=360,
							   interval=intervalo,
							   blit=True)

							   

plt.show()
