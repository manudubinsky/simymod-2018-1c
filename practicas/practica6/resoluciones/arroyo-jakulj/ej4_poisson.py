import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter

def inv_densidad_exponencial(l, u):
    """
    l: lambda
    u: 0 .. 1
    return: 0 .. +inf
    """
    return -np.log(1 - u) / l
    
def gen_exponencial(l):
    """
    genera una funcion que devuelve un numero al azar ~ Exp(l)
    l: lambda
    return: funcion() -> float ~ Exp(l)
    """
    def exponencial():
        u = np.random.rand()                # numero al azar ~ Unif(0,1)
        x = inv_densidad_exponencial(l, u)  # mapeamos Unif(0,1) -> Exp(l)
        return x
   
    return exponencial

def gen_poisson(l, limite):
    """
    genera una funcion que devuelve un numero al azar ~ Poisson()
    l: lambda
    return: funcion() -> int ~ Poisson(l)
    """
    exponencial = gen_exponencial(l)
    
    def poisson():
        n = 0
        acc = 0.0
        while acc < limite: # loop hasta pasarse del limite
            e = exponencial() # numero al azar ~ Exp(l)
            acc += e
            if acc < limite:
                n += 1
        return n
   
    return poisson

def main():
    if len(sys.argv) != 4:
        raise Exception("usage: " + sys.argv[0] + " cant lambda limite")
    
    cant = int(sys.argv[1])
    l = float(sys.argv[2])
    limite = float(sys.argv[3])
    
    poisson = gen_poisson(l, limite)
    
    v = np.zeros(cant)
    for i in range(0, len(v)):
        v[i] = poisson()
    
    c = Counter(v)
    
    #x = np.zeros(c.keys().max(), dtype=float)
    #y = np.zeros(c.keys().max(), dtype=float)
    
    x = np.array(c.keys())
    y = np.array(c.values(), dtype=float)
    
    plt.bar(x, y, facecolor='r')
    plt.axis([0, x.max() + 1.0, 0, y.max()])
    #plt.xticks(np.arange(0, x.max() + 1, x.max() / 10))
    plt.show()
    
    #n, bins, patches = plt.hist(v, 100, density=True, facecolor='g', alpha=0.75)
    #plt.show()

main()
