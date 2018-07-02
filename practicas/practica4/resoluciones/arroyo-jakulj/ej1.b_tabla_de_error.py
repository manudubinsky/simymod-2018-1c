import numpy as np
import matplotlib.pyplot as plt
import math as m


def D_mas(u, h, x):
    return ( u(x + h) - u(x) ) / h
    
def D_menos(u, h, x):
    return ( u(x) - u(x - h) ) / h

def D_0(u, h, x):
    return ( u(x + h) - u(x - h) ) / (2*h)



def u(x):
    return m.sin(x) + m.cos(x)

def u1(x):
    return m.cos(x) - m.sin(x)


x = 1

hs = [1.0e-1, 5.0e-2, 1.0e-2, 5.0e-3, 1.0e-3]


for h in hs:
    d_mas = u1(x) - D_mas(u, h, x)
    d_menos = u1(x) - D_menos(u, h, x)
    d_0 = u1(x) - D_0(u, h, x)
    
    print h, '\t', d_mas, '\t', d_menos, '\t', d_0

