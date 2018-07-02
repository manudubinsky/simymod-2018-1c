#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def i(x):
    return 2 * math.sin(x)


def wave_function(x, t, dx, dt, c, I):
    # Given mesh points as arrays x and t (x[i], t[n])
    cont = 0
    C = c * dt / dx  # Courant number
    Nt = len(t) - 1
    Nx = len(x) - 1

    z = np.zeros((len(t), len(x)))
    u_n = np.zeros(Nx + 1)
    u = np.zeros(Nx + 1)
    u_nm1 = np.zeros(Nx + 1)

    # Help variable in the scheme
    # Set initial condition u(x,0) = I(x)
    for i in range(0, Nx + 1):
        u_n[i] = I(x[i])

    # Apply special formula for first step, incorporating du/dt=0
    for i in range(1, Nx):
        u[i] = u_n[i] + 0.5 * (C ** 2) * (u_n[i + 1] - 2 * u_n[i] + u_n[i - 1])
    u[0] = 0
    u[Nx] = 0

    # matriz z
    z[0] = u

    # Enforce boundary conditions
    # Switch variables before next step

    u_nm1[:] = u_n
    u_n[:] = u
    for n in range(1, Nt):
        # Update all inner mesh points at time t[n+1]
        for i in range(1, Nx):
            u[i] = 2 * u_n[i] - u_nm1[i] + (C ** 2) * (
                    u_n[i + 1] - 2 * u_n[i] + u_n[i - 1])
        # Insert boundary conditions
        u[0] = 0
        u[Nx] = 0

        # matriz z
        z[n] = u
        # Switch variables before next step
        u_nm1[:], u_n[:] = u_n, u

    return z


x = np.linspace(0, 10, 11)
t = np.linspace(0, 100, 101)
z = wave_function(x, t, 1, 1, 1, i)

x3D, t3D = np.meshgrid(x, t)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line = ax.plot_surface(x3D, t3D, z,color= 'b')
plt.show()

# z = wave_function(x, t, 1, 1, 0.5, i)
# line = ax.plot_surface(x3D, t3D, z,color= 'b')
# plt.show()
#
# z = wave_function(x, t, 1, 1, 2, i)
# line = ax.plot_surface(x3D, t3D, z,color= 'b')
# plt.show()