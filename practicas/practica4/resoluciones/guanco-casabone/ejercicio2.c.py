import numpy as np
import matplotlib.pyplot as plt

def cooling(T0, k, t_end, dt, theta=0.5):
    dt = float(dt)
    Nt = int(round(t_end/dt))
    T = Nt*dt
    u = np.zeros(Nt+1)
    t = np.linspace(0, t_end, Nt+1)
    u[0] = T0
    for n in range(0, t_end):
        if n <= (3/k):
            T_s = 2*T0
        else:
            T_s = 0.5*T0

        u[n+1] = (u[n] + dt*(theta*-k*T_s + (1 - theta)*(-k*u[n] + k*T_s)))/(1 + k*theta*dt)
    return u, t

u, t = cooling(2500, 4, 10, 1, 0.5)

plt.plot(t, u, 'b')

plt.show()
