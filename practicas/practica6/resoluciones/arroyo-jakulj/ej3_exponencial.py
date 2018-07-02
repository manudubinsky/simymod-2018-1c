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

def main():
    if len(sys.argv) != 3:
        raise Exception("usage: " + sys.argv[0] + " cant lambda")
    
    cant = int(sys.argv[1])
    l = float(sys.argv[2])
    
    exponencial = gen_exponencial(l)
    
    v = np.zeros(cant)
    for i in range(0, len(v)):
        v[i] = exponencial()
    
    #c = Counter(v)
    
    #x = np.array(c.keys())
    #y = np.array(c.values(), dtype=float) / cant
    
    #plt.bar(x, y, facecolor='r')
    #plt.axis([0, x.max() + 1.0, 0, y.max()])
    #plt.xticks(np.arange(0, x.max() + 1, 1.0))
    #plt.show()
    
    n, bins, patches = plt.hist(v, 100, density=True, facecolor='g', alpha=0.75)
    plt.show()

main()
