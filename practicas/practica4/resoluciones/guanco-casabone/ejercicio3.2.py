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
        u[n+1] = (u[n] + dt*(theta*-k*T_s + (1.0 - theta)*(-k*u[n] + k*T_s)))/(1.0 + k*theta*dt)
    return u, t

u, t = cooling(37, 0.134, 20, 8, 1, 0)
# u, t = cooling(37, 0.155, 20, 4, 1, 1)
# u, t = cooling(37, -2.0, 20.0, 4, 1, 0.5)
print u
plt.plot(t, u, 'b')

plt.show()
