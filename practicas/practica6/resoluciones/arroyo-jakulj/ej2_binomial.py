import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter

def gen_binomial(n, p):
    def binomial():
        x = 0
        for i in range(0, n):
            a = np.random.rand()
            if a <= p:
                x = x + 1
        return x
            
    return binomial

def main():
    if len(sys.argv) != 4:
        raise Exception("usage: " + sys.argv[0] + " cant n P(H)")
    
    cant = int(sys.argv[1])
    n = int(sys.argv[2])
    p = float(sys.argv[3])
    
    binomial = gen_binomial(n, p)
    
    x = np.zeros(cant)
    for i in range(0, len(x)):
        x[i] = binomial()
    
    c = Counter(x)
    
    x = np.array(c.keys())
    y = np.array(c.values(), dtype=float) / cant
    
    plt.bar(x, y, facecolor='g')
    plt.show()

main()
