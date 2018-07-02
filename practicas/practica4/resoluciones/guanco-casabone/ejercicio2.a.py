import numpy as np
import matplotlib.pyplot as plt

def cooling(T0, k, T_s, t_end, dt, theta=0.5):
    dt = float(dt)
    Nt = int(round(t_end/dt))
    T = Nt*dt
    u = np.zeros(Nt+1)
    t = np.linspace(0, t_end, Nt+1)
    u[0] = T0
    for n in range(0, t_end):
        u[n+1] = (u[n] + dt*(theta*-k*T_s + (1 - theta)*(-k*u[n] + k*T_s)))/(1 + k*theta*dt)
    return u, t

u, t = cooling(100, 2, 1, 100, 1, 0)
u2, t2 = cooling(100, 2, 1, 10, 1, 1)
u3, t3 = cooling(100, 2, 1, 10, 1, 0.5)

#plt.plot(t, u, 'b')
plt.plot(t2, u2, 'r')
plt.plot(t3, u3, 'g')
plt.show()
