import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter

def gen_pascal(m, p):
    def pascal():
        x = 0
        n = 0
        while x < m:
            a = np.random.rand()
            if a <= p:
                x = x + 1
            n = n + 1
        return n
   
    return pascal

def main():
    if len(sys.argv) != 4:
        raise Exception("usage: " + sys.argv[0] + " cant m P(H)")
    
    cant = int(sys.argv[1])
    m = int(sys.argv[2])
    p = float(sys.argv[3])
    
    pascal = gen_pascal(m, p)
    
    x = np.zeros(cant)
    for i in range(0, len(x)):
        x[i] = pascal()
    
    c = Counter(x)
    
    x = np.array(c.keys())
    y = np.array(c.values(), dtype=float) / cant
    
    plt.bar(x, y, facecolor='b')
    plt.axis([0, x.max() + 1.0, 0, y.max()])
    plt.xticks(np.arange(0, x.max() + 1, 1.0))
    plt.show()

main()
