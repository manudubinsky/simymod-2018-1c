import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    cant = 100

    if len(sys.argv) == 2:
        cant = int(sys.argv[1])
        
    x = np.random.rand(cant)
    
    n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)
    plt.show()

main()
