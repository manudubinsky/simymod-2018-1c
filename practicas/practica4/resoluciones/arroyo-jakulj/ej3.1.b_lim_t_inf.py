import numpy as np
import matplotlib.pyplot as plt
import math as m

"""
Ejercicio 3
En base a la implementacion en la seccion 1.1 del libro 2 (pag. 15):
1. Realizar los puntos a), b) y c) del ejercicio 4.3 (pag 113)
    b) In the case lim(t->inf) T_s(t) = C = const, explain why T(t) -> C
    
    Respuesta: la derivada de T:
        T'(t) = -k*(T(t) - T_s(t))
    indica que la derivada T' es negativa mientras T(t) > T_s(t), por lo que
    T(t) disminuira acercandose a T_s(t) asintoticamente. mientras que dt sea lo
    suficientemente pequenio, T(t) nunca llegara a T_s(t) = C
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
    num_points = int(m.floor(t_end / dt)) + 1
    t = np.zeros(num_points, dtype=float)
    for i in range(0, num_points):
        t[i] = i * dt
    
    T = discretizar_funcion(k, T0, T_s, t, theta)
    
    return T, t
    

def main():
    # coeff transferencia
    k = 0.1
    
    # temperatura inicial del objeto = 300 K
    T0 = 300
    
    # temperatura del rededor: inicia en 200, termina en 100 const
    T_s = lambda t: 100 / (t + 1) + 100
    
    
    # puntos del tiempo
    t_end = 200.0
    dt = 1.0

    # Theta para crank-nicolson
    theta = 0.5
    
    
    T, t = cooling(T0, k, T_s, t_end, dt, theta)
    
    
    plt.plot(t, T)
    plt.show()
    
    
main()
