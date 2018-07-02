import numpy as np
import matplotlib.pyplot as plt
import math as m

"""
Ejercicio 2
En base a los tres esquemas descriptos en la seccion 1.1 del libro 2 (Forward
Euler, Backward Euler, Crank-Nicholson), realizar discretizaciones para el
ejercicio 4.2 (pag. 112)
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


def main():
    k = 0.1
    T0 = 300            # temperatura inicial del objeto = 300 K
    Ts = lambda t: 200  # temperatura del rededor = 200 K constante
    
    # puntos del tiempo: 0.0, 0.1, ..., 10.0
    # cantidad de puntos discretizados
    NUM_PUNTOS = 100
    # cantidad de segundos
    TMP_SIMULADO = 100.0
    t = np.zeros(NUM_PUNTOS, dtype=float)
    for i in range(0, NUM_PUNTOS):
        t[i] = (TMP_SIMULADO / NUM_PUNTOS) * i

    th = 0.5            # Theta para crank-nicolson
    
    
    T = discretizar_funcion(k, T0, Ts, t, th)
    
    
    plt.plot(t, T)
    plt.show()
    
    
main()
