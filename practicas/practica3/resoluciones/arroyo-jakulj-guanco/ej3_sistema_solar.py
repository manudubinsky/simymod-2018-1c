#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import math

# constantes
tmes = 4
tdia = tmes / 28.0
tanio = 12.0 * tmes

factor_radio_sol = 0.2
factor_radio_planeta = 10
factor_radio_satelite = 10
factor_orbita_planeta = 0.01
factor_orbita_satelite = 0.5


radio_sol = 691000 * factor_radio_sol
radio_mercurio = 2439 * factor_radio_planeta
radio_venus = 6051 * factor_radio_planeta
radio_tierra = 6371 * factor_radio_planeta
radio_luna = 1737 * factor_radio_satelite
radio_marte = 3397 * factor_radio_planeta
radio_phobos = radio_luna #13 * factor_radio_satelite
radio_deimos = radio_luna #6 * factor_radio_satelite

orbita_sol = 0
orbita_mercurio = 57894376 * factor_orbita_planeta
orbita_venus = 108208930 * factor_orbita_planeta
orbita_tierra = 149597000 * factor_orbita_planeta
orbita_luna = 384400 * factor_orbita_satelite
orbita_marte = 227936640 * factor_orbita_planeta
orbita_phobos = orbita_luna/2# 9377 * factor_orbita_satelite
orbita_deimos = orbita_luna # 23460 * factor_orbita_satelite

w_sol = 0
w_mercurio = (2 * math.pi) / (87 * tdia)
w_venus = (2 * math.pi) / (224 * tdia)
w_tierra = (2 * math.pi) / tanio
w_luna = (2 * math.pi) / tmes
w_martes = (2 * math.pi) / (687 * tdia)
w_phobos = (2 * math.pi) / (0.31891023 * tdia)
w_deimos = (2 * math.pi) / (1262 * tdia)

limite = orbita_marte

intervalo = 20
dt = 0.001 * intervalo

# globales
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-limite, limite), ylim=(-limite, limite))
sol = plt.Circle((0,0), radius = radio_sol, fc='y')
mercurio = plt.Circle((0,0), radius = radio_mercurio, fc=(0.25,0.25,0.25))
venus = plt.Circle((0,0), radius = radio_venus, fc='m')
tierra = plt.Circle((0,0), radius = radio_tierra, fc='b')
luna = plt.Circle((0,0), radius = radio_luna, fc=(0.75,0.75,0.75))
marte = plt.Circle((0,0), radius = radio_marte, fc='r')
phobos = plt.Circle((0,0), radius = radio_phobos, fc='k')
deimos = plt.Circle((0,0), radius = radio_deimos, fc='b')

tiempo_transcurrido = 0

def init():
	sol.center = (0,0)
	mercurio.center = (0,0)
	venus.center = (0,0)
	tierra.center = (0,0)
	luna.center = (0,0)
	marte.center = (0,0)
	phobos.center = (0,0)
	deimos.center = (0,0)
	ax.add_patch(sol)
	ax.add_patch(mercurio)
	ax.add_patch(venus)
	ax.add_patch(tierra)
	ax.add_patch(luna)
	ax.add_patch(marte)
	ax.add_patch(phobos)
	ax.add_patch(deimos)
	return mercurio, venus, tierra, luna, marte, phobos, deimos,

def animate(i):
	global tiempo_transcurrido, orbita_luna, orbita_tierra, orbita_mercurio, orbita_venus, orbita_marte, orbita_phobos, orbita_deimos
	tiempo_transcurrido += dt
	
	# sol
	sx, sy = sol.center
	
	# mercurio
	mx, my = mercurio.center
	angulo = w_mercurio * tiempo_transcurrido
	mx = math.cos(angulo) * orbita_mercurio + sx
	my = math.sin(angulo) * orbita_mercurio + sy
	mercurio.center = (mx, my)
	
	# venus
	vx, vy = venus.center
	angulo = w_venus * tiempo_transcurrido
	vx = math.cos(angulo) * orbita_venus + sx
	vy = math.sin(angulo) * orbita_venus + sy
	venus.center = (vx, vy)
	
	# tierra
	tx, ty = tierra.center
	angulo = w_tierra * tiempo_transcurrido
	tx = math.cos(angulo) * orbita_tierra + sx
	ty = math.sin(angulo) * orbita_tierra + sy
	tierra.center = (tx, ty)
	
	# luna
	lx, ly = luna.center
	angulo = w_luna * tiempo_transcurrido
	lx = math.cos(angulo) * orbita_luna + tx
	ly = math.sin(angulo) * orbita_luna + ty
	luna.center = (lx, ly)
	
	# marte
	mx, my = marte.center
	angulo = w_martes * tiempo_transcurrido
	mx = math.cos(angulo) * orbita_marte + sx
	my = math.sin(angulo) * orbita_marte + sy
	marte.center = (mx, my)
	
	# phobos
	px, py = phobos.center
	angulo = w_phobos * tiempo_transcurrido
	px = math.cos(angulo) * orbita_phobos + mx
	py = math.sin(angulo) * orbita_phobos + my
	phobos.center = (px, py)
	
	# deimos
	dx, dy = deimos.center
	angulo = w_deimos * tiempo_transcurrido
	dx = math.cos(angulo) * orbita_deimos + mx
	dy = math.sin(angulo) * orbita_deimos + my
	deimos.center = (dx, dy)
	
	return mercurio, venus, tierra, luna, marte, phobos, deimos,

anim = animation.FuncAnimation(fig, animate, 
							   init_func=init, 
							   frames=360,
							   interval=intervalo,
							   blit=True)

plt.show()
