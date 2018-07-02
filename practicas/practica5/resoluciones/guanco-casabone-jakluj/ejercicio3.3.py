#!/usr/bin/python

import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib.animation as animation


class WaveFunction:
    def __init__(self, x ,t, dx, dt, c, I):
        self.x = x
        self.t = t
        self.dx = dx
        self.dt = dt
        self.c = c
        self.I = I
        self.C = c*dt/dx
        self.Nt = len(self.t) - 1
        self.Nx = len(self.x) - 1
        self.u_n = np.zeros(self.Nx + 1, dtype=float)
        self.u = np.zeros(self.Nx + 1, dtype=float)
        self.u_nm1 = np.zeros(self.Nx + 1, dtype=float)


    def initialCondition(self):
        # Help variable in the scheme
        # Set initial condition u(x,0) = I(x)
        for i in range(0, self.Nx + 1):
            self.u_n[i] = self.I(x[i])
        self.u_n[0] = 0
        self.u_n[self.Nx] = 0
        return self.u_n


    def firstStep(self):
        # Apply special formula for first step, incorporating du/dt=0
        for i in range(1, self.Nx):
            # self.u[i] = 0.5*(self.u_n[i + 1] + self.u_n[i - 1])
            self.u[i] = self.u_n[i] + 0.5*(self.C**2)*(self.u_n[i + 1] - 2*self.u_n[i] + self.u_n[i - 1])
        self.u[0] = 0
        self.u[self.Nx] = 0
        self.u_nm1[:] = self.u_n
        self.u_n[:] = self.u

        return self.u


    def nextStep(self):
        # Update all inner mesh points at time t[n+1]
        for i in range(1, self.Nx):
            # self.u[i] = -1*self.u_nm1[i] + self.u_n[i+1] + self.u_n[i-1]
            self.u[i] = 2 * self.u_n[i] - self.u_nm1[i] + (self.C ** 2) * (
                        self.u_n[i + 1] - 2 * self.u_n[i] + self.u_n[i - 1])
        # Insert boundary conditions
        self.u[0] = 0
        self.u[self.Nx] = 0
        # Switch variables before next step
        self.u_nm1[:], self.u_n[:] = self.u_n, self.u
        return self.u_n


def i(x):
    return 1 if 0 <= x <= 1 else 0


fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(-2, 2))
x = np.linspace(0, 10, 11)
t = np.linspace(0, 20, 21)

wave = WaveFunction(x, t, 1, 0.1, 1, i)
line, = ax.plot(x, wave.initialCondition())


def animate(i):
    global wave
    if i == 1:
        line.set_ydata(wave.firstStep())
    elif i != 0 and i != 1:
        line.set_ydata(wave.nextStep())
    return line,


ani = animation.FuncAnimation(fig, animate, interval=21, blit=False)
plt.show()