import numpy as np
import matplotlib.pyplot as plt
import math as m



# funciones para las derivadas discretas
def D_mas(u, h, x):
    return ( u(x + h) - u(x) ) / h
    
def D_menos(u, h, x):
    return ( u(x) - u(x - h) ) / h

def D_0(u, h, x):
    return ( u(x + h) - u(x - h) ) / (2*h)



# funcion u que vamos a estudiar
def u(x):
    return m.sin(x) + m.cos(x)

def u1(x):
    return m.cos(x) - m.sin(x)



x = 1

hs = [1.0e-1, 5.0e-2, 1.0e-2, 5.0e-3, 1.0e-3]

errores = np.zeros((3,len(hs)),dtype=float)

i = 0
for h in hs:
    d_mas = u1(x) - D_mas(u, h, x)
    d_menos = u1(x) - D_menos(u, h, x)
    d_0 = u1(x) - D_0(u, h, x)
    
    print h, '\t', d_mas, '\t', d_menos, '\t', d_0
    
    errores[0, i] = d_mas
    errores[1, i] = d_menos
    errores[2, i] = d_0
    
    i += 1


line = plt.loglog(hs, np.abs(errores[0]))
plt.setp(line, label='D+')
plt.loglog(hs, np.abs(errores[1]))
plt.loglog(hs, np.abs(errores[2]))
#plt.axis(np.abs([np.min(hs), np.max(hs), np.min(errores), np.max(errores)]))
#plt.ylabel('error')
plt.grid(True)

plt.show()
