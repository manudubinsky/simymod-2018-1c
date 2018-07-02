import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter

def gen_poisson(l):
    def Px(k):
        return (math.e**-l) * 
    
    def poisson():
        
        b_left = b
        r_left = r
        for i in range(0, k):
            a = np.random.rand()
            p = (1.0 * b_left / (b_left + r_left))
            if a < p:
                x += 1
                b_left -= 1
            else:
                r_left -= 1
        return x
   
    return poisson

def main():
    if len(sys.argv) != 5:
        raise Exception("usage: " + sys.argv[0] + " cant b r k")
    
    cant = int(sys.argv[1])
    b = int(sys.argv[2])
    r = int(sys.argv[3])
    k = int(sys.argv[4])
    
    poisson = gen_poisson(b, r, k)
    
    v = np.zeros(cant)
    for i in range(0, len(v)):
        v[i] = poisson()
    
    c = Counter(v)
    
    x = np.array(c.keys())
    y = np.array(c.values(), dtype=float) / cant
    
    plt.bar(x, y, facecolor='r')
    plt.axis([0, x.max() + 1.0, 0, y.max()])
    plt.xticks(np.arange(0, x.max() + 1, 1.0))
    #print v
    plt.show()

main()
