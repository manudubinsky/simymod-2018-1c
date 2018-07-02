import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

################################################################################
# globales
################################################################################
dt = 0.05
dx = 1.0

Nt = 20
Nx = 32

t = np.linspace(0, Nt*dt, Nt+1)
x = np.linspace(0, Nx*dx, Nx+1)

max_x = max(x)

u = np.zeros((Nt+1, Nx+1), dtype=float)

c = None
C = None
C2 = None

I = None

################################################################################
# funciones
################################################################################
def polynom(x):
    x = 10.0 / max_x * x
    return -(0.2)*(x**2) + (2.0*x)
    """
    f(x) = -0.2 * x^2 + 2.0 * x
    f'(x) = -0.4 * x + 2.0
    
    f'(x) = 0
    -0.4*x+2.0 = 0
    -0.4*x = -2.0
    x = -2.0 / -0.4
    x = -5.0
    
    x1 = 0
    x2 = 10
    """

def sin(x):
    w = 2.0 / max_x
    return 2 * math.sin(math.pi * x * w)

def sinc(x):
    return 2 * math.sin(math.pi * x) / (math.pi * x)

def cuadrado(x):
    if x <= 1.0:
        return 1.0
    else:
        return 0.0

################################################################################
# resolucion
################################################################################
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

################################################################################
# graficar
################################################################################
def print_usage(path):
    print \
        "usage:", path, "modo c\n" \
        "  modo:\n" \
        "    poly        Graficar polinomi\n" \
        "    sin         Graficar seno\n" \
        "    sinc        Graficar sinc\n" \
        "    cuadrado    Graficar un cuadrado\n" \
        "  c:\n" \
        "    Constante c\n" \
        ""
        

def main():
    global I, c, u, x, t, C, C2, Nt, Nx
    
    path = sys.argv[0]
    
    if len(sys.argv) != 3:
        print_usage(path)
        return
    
    modo = sys.argv[1]
    
    I = None
    c = None
    
    if modo == "help":
        print_usage(path)
        return        
    elif modo == "poly":
        I = polynom
    elif modo == "sin":
        I = sin
    elif modo == "sinc":
        I = sinc
    elif modo == "cuadrado":
        I = cuadrado
    else:
        print("modo incorrecto")
        print_usage(path)
        return
    
    try:
        c = float(sys.argv[2])
    except:
        print("valor de 'c' incorrecto")
        print_usage(path)
        return
    
    C = c*dt/dx
    C2 = C**2

    for n in range(0, Nt+1):
        calcular(n)

    n = 2.*np.pi
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #x = np.linspace(0,n,100)
    #y = np.linspace(0,n,100)
    #x,y = np.meshgrid(x,y)
    #z = np.sin(x+y)
    #line = ax.plot_surface(x, y, z,color= 'b')
    
    xx, tt = np.meshgrid(x, t)
    uu = np.zeros((len(x), len(t)), dtype=float)
    for it in range(0, len(u)):
        for ix in range(0, len(u[it])):
            uu[ix, it] = u[it, ix]
            
    line = ax.plot_surface(xx, tt, u, color='g')

    plt.show()
    
main()
