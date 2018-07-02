import numpy as np


# globales
dt = 1.0
dx = 1.0

Nt = 2
Nx = 100

t = [i*dt for i in range(0, Nt + 1)]
x = [i*dx for i in range(0, Nx + 1)]

max_x = max(x)

u = np.zeros((Nt+1, Nx+1), dtype=float)

c = 1
C = c*dt/dx             # Courant number
C2 = C**2               # Help variable in the scheme


def I(x):
    cima = 7
    a = cima / (max_x / 2)
    if x < max_x / 2:
        return a * x
    else:
        return a * (max_x - x)


def calcular(n):
    if n == 0:
        calcular_inicial()
    elif n == 1:
        calcular_n_1()
    else:
        calcular_siguiente(n-1)


def calcular_inicial():
    # Set initial condition u(x,0) = I(x)
    for i in range(1, Nx):
        u[0][i] = I(x[i])
    u[0][0] = 0
    u[0][Nx] = 0


def calcular_n_1():
    # Apply special formula for first step, incorporating du/dt=0
    for i in range(1, Nx):
        a = u[0][i] + \
                0.5*(C**2)*(u[0][i+1] - 2*u[0][i] + u[0][i-1])
        u[1][i] = a
    u[1][0] = 0; u[1][Nx] = 0     # Enforce boundary conditions


def calcular_siguiente(n):
    # Switch variables before next step
    u_n = u[n]
    u_nm1 = u[n-1]
    u_np1 = u[n+1]
    
    # Update all inner mesh points at time t[n+1]
    for i in range(1, Nx):
        u_np1[i] = 2*u_n[i] - u_nm1[i] + \
                (C**2)*(u_n[i+1] - 2*u_n[i] + u_n[i-1])
    
    # Insert boundary conditions
    u_np1[0] = 0; u_np1[Nx] = 0


for n in range(0, Nt+1):
    calcular(n)

print u
