import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter

def gen_box_muller_cos(sigma, mu):
    """
    genera una funcion que devuelve un numero al azar
    aproximado a ~ Normal(sigma, mu)
    * utiliza cos
    return: funcion() -> float ~ Normal(sigma, mu)
    """
    def box_muller():
        u = np.random.rand()                # numero al azar ~ Unif(0,1)
        v = np.random.rand()                # numero al azar ~ Unif(0,1)
        r = np.sqrt(-2.0 * np.log(u)) * np.cos(2.0 * np.pi * v);
        return r
   
    return box_muller
    
def gen_box_muller_sin(sigma, mu):
    """
    genera una funcion que devuelve un numero al azar
    aproximado a ~ Normal(sigma, mu)
    * utiliza sin
    return: funcion() -> float ~ Normal(sigma, mu)
    """
    def box_muller():
        u = np.random.rand()                # numero al azar ~ Unif(0,1)
        v = np.random.rand()                # numero al azar ~ Unif(0,1)
        r = np.sqrt(-2.0 * np.log(u)) * np.sin(2.0 * np.pi * v);
        return r
   
    return box_muller

def main():
    if len(sys.argv) != 4:
        raise Exception("usage: " + sys.argv[0] + " cant sigma mu")
    
    cant = int(sys.argv[1])
    sigma = float(sys.argv[2])
    mu = float(sys.argv[3])
    
    
    box_muller_sin = gen_box_muller_sin(sigma, mu)
    
    v1 = np.zeros(cant)
    for i in range(len(v1)):
        v1[i] = box_muller_sin()
    
    
    box_muller_cos = gen_box_muller_cos(sigma, mu)
    
    v2 = np.zeros(cant)
    for i in range(len(v2)):
        v2[i] = box_muller_cos()
    
    
    n, bins, patches = plt.hist((v1,v2), 100, density=True, alpha=0.75)
    plt.show()

main()
