import numpy as np
import matplotlib.pyplot as plt
import sys

def gen_geometric(p):
    def geometric():
        a = np.random.rand()
        if a <= p:
            return 1
        else:
            return 1 + geometric()
            
    return geometric

def main():
    if len(sys.argv) != 3:
        raise Exception("usage: " + sys.argv[0] + " cant P(H)")
    
    cant = int(sys.argv[1])
    p = float(sys.argv[2])
    
    geometric = gen_geometric(p)
        
    x = np.zeros(cant)
    for i in range(0, len(x)):
        x[i] = geometric()
        
    n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)
    plt.show()

main()
