import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math as m

"""
Ejercicio 4
"""

def theta_rule(a, u, h, t, n, th):
    """
    Implementacion del esquema Theta-Rule para discretizar una funcion como Forward
    Euler, Backward Euler o Crank-Nicholson.
    
    requiere:
        u'(tn) = -a*(u(tn) - h(tn))

        t[n] y t[n+1] tiene valor
        u[n] tiene valor
        h(t[n]) y h(t[n+1]) tienen valor
        a(t[n]) y a(t[n+1]) tienen valor
    
    devuelve: u(t[n+1])
    
    a: funcion de magnitud de la derivada
    u: lista con los puntos ya discretizados de la imagen; u[0] == I
    h: funcion desviacion de la funcion u
    t: lista con los puntos discretizados del dominio (tiempo)
    n: punto que queremos discretizar
    th: Theta
    """
    
    Dt = t[n+1] - t[n]
    num = (1.0 - (1-th)*a*Dt)*u[n] + (1-th)*a*Dt*h(t[n]) + th*a*Dt*h(t[n+1])
    den = 1 + th*a*Dt
    
    return num/den


def discretizar_funcion(a, I, h, t, th):
    """
    Obetener una lista de temperaturas en los puntos de tiempo t.
    
    devuelve: una lista con los puntos discretizados
    
    a: constante de transferencia
    I: valor inicial
    h: funcion de desviacion
    t: lista con los puntos discretizados del dominio (tiempo)
    th: Theta
    """
    
    u = np.zeros(len(t), dtype=float)
    u[0] = I
    for n in range(0, len(t) - 1):
        u[n+1] = theta_rule(a, u, h, t, n, th)
    return u


def cooling(T0, k, T_s, t_end, dt, theta=0.5):
    """
    returns:
        (T, t)
        T: array of values ate mesh points
        t: array of time mesh
       
    params:
        T0: initial temperature
        k: heat transfer coefficient
        T_s: function of t for temperature of surroundings
        T_end: end time of simultion
        dt: time step
        theta: theta for theta-rule
    """
    
    # rounded down + initial point
    t = np.arange(0.0, t_end, dt)
    T = discretizar_funcion(k, T0, T_s, t, theta)
    
    return T, t
    
################################################################################
    
# coeff transferencia
k = 0.9/6.7

# temperatura inicial del objeto
T0 = 37.0

# temperatura del rededor
T_s = lambda t: 20.0


# puntos del tiempo
t_end = 48.0 # 48 horas
dt = 0.1

# Theta para crank-nicolson
theta = 0.5


T, t = cooling(T0, k, T_s, t_end, dt, theta)

T_min = T[0]
T_max = T[0]
for n in range(0, len(t)):
    if T[n] < T_min:
        T_min = T[n]
        
    if T[n] > T_max:
        T_max = T[n]
        
    if T_s(t[n]) < T_min:
        T_min = T_s(t[n])
        
    if T_s(t[n]) > T_max:
        T_max = T_s(t[n])

################################################################################

# globales
intervalo = 5

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-2.0, 2.0), ylim=(-2.0, 2.0))
cir = plt.Circle((0,0), radius=1.0, fc='y')

def temp_to_RGB(temp, temp_min, temp_max):
    x = (temp - temp_min) / (temp_max - temp_min)
    return (x, 0.0, 1.0-x)

def init():
    global ax, cir
    cir.center = (0,0)
    ax.add_patch(cir)
    
    ax.set_facecolor(temp_to_RGB(T_s(t[0]), T_min, T_max))
    cir.set_facecolor(temp_to_RGB(T[0], T_min, T_max))
    
    return ax, cir,

def animate(n):
    global ax, cir, T_s, t, T_min, T_max, T
    
    ax.set_facecolor(temp_to_RGB(T_s(t[n]), T_min, T_max))
    cir.set_facecolor(temp_to_RGB(T[n], T_min, T_max))
    
    return cir,


anim = animation.FuncAnimation(fig, animate, 
                               blit=False,
                               interval=intervalo,
                               init_func=init, 
                               frames=len(t))

plt.show()

