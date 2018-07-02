#!/usr/bin/python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import animation

def waveFunction(x, t, dx, dt, T, L, c, I):

	# Given mesh points as arrays x and t (x[i], t[n])
	C = c*dt/dx # Courant number
	Nt = len(t)-1
	Nx = len(x)-1
	C2 = C**2 # Help variable in the scheme

	u_n = np.zeros(Nx+1)
	u = np.zeros(Nx+1)
	u_nm1 = np.zeros(Nx+1)

	# Help variable in the scheme
	# Set initial condition u(x,0) = I(x)
	for i in range(0, Nx+1):
		u_n[i] = I(x[i])

	# Apply special formula for first step, incorporating du/dt=0
	for i in range(1, Nx):
		u[i] = u_n[i] - 0.5*C**2*(u_n[i+1] - 2*u_n[i] + u_n[i-1])
	u[0] = 0; u[Nx] = 0

	# Enforce boundary conditions
	# Switch variables before next step

	u_nm1[:] = u_n
	u_n[:] = u
	for n in range(1, Nt):
		# Update all inner mesh points at time t[n+1]
		for i in range(1, Nx):
			u[i] = 2*u_n[i] - u_nm1[i] - C**2*(u_n[i+1] - 2*u_n[i] + u_n[i-1])
		# Insert boundary conditions
		u[0] = 0; u[Nx] = 0
		print u
		# print "--------"
		print x
		print "--------"
		# Switch variables before next step
		u_nm1[:], u_n[:] = u_n, u

	return u_nm1, u_n

def I(x):
	return x*2

x = np.linspace(0, 10, 10+1)
t = np.linspace(0, 20, 20+1)

u, u_n = waveFunction(x, t, 1, 1, 20, 10, 2, I)
