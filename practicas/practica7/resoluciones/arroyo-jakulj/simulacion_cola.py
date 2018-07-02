import time  as tp
import numpy as np
import Queue as qp
import sys
import math

from collections import Counter

################################################################################

# simulate realtime
realtime = False
# display states
displaying = False

################################################################################

def rand_exponencial(lamb):
    u = np.random.rand() # :: 0..1
    return -np.log(1.0 - u) / lamb # :: 0..1 -> 0..+inf

class Client:
    def __init__(self, arrived):
        self.arrive = arrived
        self.served = None
        self.left = None

class Event():
    def __init__(self, time):
        self.time = time
        
    def proc(self):
        pass
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __str__(self):
        pass
    
class ArriveEv(Event):
    def __init__(self, time, q):
        Event.__init__(self, time)
        self.q = q
    
    def proc(self):
        c = Client(self.q.sy.time)
        self.q.sy.arrives(c)
    
    def __str__(self):
        return "Arrive(" + str(self.time) + "," + str(self.q) + ")"
        
class LeaveEv(Event):
    def __init__(self, time, s):
        Event.__init__(self, time)
        self.s = s
        
    def proc(self):
        self.s.sy.leaves(self.s)
        
    def __str__(self):
        return "Leave(" + str(self.time) + "," + str(self.s) + ")"
        
class Q:
    def __init__(self, sy, lam):
        self.sy = sy
        self.lam = lam
        self.clients = qp.Queue()
        
    def __str__(self):
        return "Q(n=" + str(len(self.clients.queue)) + ")"
        
    def gen_time_for_next_client(self):
        n = self.sy.compute_n()
        #return rand_exponencial(self.lam(n))
        return rand_exponencial(self.lam)
    
    def create_arrive_event(self):
        time = self.sy.time + self.gen_time_for_next_client()
        self.sy.add_event(ArriveEv(time, self))
    
    def arrives(self, client):
        self.clients.put(client)
        self.create_arrive_event()
    
    def remove(self):
        return self.clients.get()

class S:
    def __init__(self, sy, id, mu):
        self.sy = sy
        self.id = id
        self.mu = mu
        self.client = None
   
    def __str__(self):
        return "S(id=" + str(self.id) + ",c=" + str(1 if self.client else 0) + ")"
        
    def gen_time_to_finish(self):
        n = self.sy.compute_n()
        #return rand_exponencial(self.mu(n))
        return rand_exponencial(self.mu)

    def create_leave_event(self):
        time = self.sy.time + self.gen_time_to_finish()
        self.sy.add_event(LeaveEv(time, self))
    
    def serve(self, client):
        self.client = client
        client.served = self.sy.time
        self.create_leave_event()
        
    def leaves(self):
        c = self.client
        self.client = None
        c.left = self.sy.time
        return c
        
class System:
    def __init__(self, lam, mu_list):
        self.q = Q(self, lam)
        self.s_list = [S(self, i, mu_list[i]) for i in range(len(mu_list))]
        self.e_list = qp.PriorityQueue()
        self.time = 0.0
        self.counter = Counter()
        self.last_P = []
        self.counter_q = Counter()
        self.veces = []
        self.last_log = 0.0
        self.history = []
        self.estado_estacionario = None
        self.eventos_procesados = 0
        
        self.q.create_arrive_event()
        
    def compute_n(self):
        qn = len(self.q.clients.queue)
        sn = sum(map(lambda s: 1 if s.client else 0, self.s_list))
        return qn + sn
    
    def add_event(self, event):
        self.e_list.put(event)
        
    def log(self):
        n = self.compute_n()
        qn = len(self.q.clients.queue)
        self.counter.update({n: self.time - self.last_log})
        self.counter_q.update({qn: self.time - self.last_log})
        self.last_log = self.time
        
        while len(self.veces) <= n:
            self.veces.append(0)
        self.veces[n] += 1
        
    
        N = max(self.counter) + 1
        P = np.zeros(N, dtype=float)
        for i in self.counter:
            P[i] = self.counter[i] / self.time
            
        mayor = False
        for i in range(len(self.last_P)):
            if abs(P[i] - self.last_P[i]) > 100.0 * sys.float_info.epsilon:
                mayor = True
                break
        if mayor:
            self.estado_estacionario = None
        else:
            self.estado_estacionario = self.eventos_procesados
        
    
    def arrives(self, c):
        self.log()
        self.q.arrives(c)
        self.try_serve_client()
    
    def leaves(self, s):
        self.log()
        c = s.leaves()
        self.history.append(c)
        self.try_serve_client()
        
    def try_serve_client(self):
        if len(self.q.clients.queue) > 0:
            for s in self.s_list:
                if not s.client:
                    c = self.q.remove()
                    s.serve(c)
                    break
    
    def proc_next_event(self):
        e = self.e_list.get()
        self.time = e.time
        e.proc()
        self.eventos_procesados += 1
    
    def proc_until(self, time):
        while self.e_list.queue[0].time < time:
            self.proc_next_event()
        self.time = time
    
    def proc_while_condition(self, cond):
        while cond(self):
            self.proc_next_event()
    
    def dump(self):
        print "time:", "{:.8f}".format(self.time), "s:", map(lambda s: 1 if s.client else 0, self.s_list), "q:", len(self.q.clients.queue)
        #print "events:", ", ".join(map(lambda e: str(e), self.e_list.queue))

################################################################################
# analisis matematico II

def P0(l,m,s):
    a = sum([1.0/math.factorial(n)*(l/m)**n for n in range(1, s+1)])
    b = (l/m)**n
    c = l**(s+1)/math.factorial(s)/m**s/(s*m-l)
    return 1.0/(1.0 + a*b + c)
    
def Lq(l, m, s):
    return l**(s+1) / math.factorial(s-1) / m**(s-1) / (s*m-l)**2 * P0(l,m,s)

def Wq(l, m, s):
    return Lq(l, m, s) / l

def W(l, m, s):
    return Wq(l, m, s) + 1/m

def L(l, m, s):
   return l * W(l, m, s)

################################################################################


def main():
    global by_event
    
    if len(sys.argv) < 3:
        print "ingrese lambda y mu como argumentos en linea de comando"
        return

    lam = float(sys.argv[1])
    mu  = float(sys.argv[2])

    lam_ = None
    mus_ = None
    
    mode = int(input("mode: "))
    
    if mode == 1:
        s = int(input("s (servers): "))
        lam_ = lam
        mus_ = [mu] * s
        
    elif mode == 2:
        s = int(input("s (divisor de lambda): "))
        lam_ = lam / s
        mus_ = [mu]
    
    elif mode == 3:
        s = int(input("s (multiplicador de mu): "))
        lam_ = lam
        mus_ = [mu*s]
    
    sy = System(lam_, mus_)
    
    print "simulando..."

    if realtime:
        time = 0.0
        dt = 0.1
        factor = 0.5
        while True:
            time += factor * dt
        
            sy.proc_until(time)
            
            if displaying:
                out = ""
                for s in sy.s_list:
                    out += "[" + ("1" if s.client else " ") + "] "
                for i in range(len(sy.q.clients.queue)):
                    out += "1"
                print out
            
            tp.sleep(dt)
    else:
        # iniciar algunos eventos 
        sy.proc_while_condition(lambda self: self.eventos_procesados < 100)
        
        # alcanzar estado estacionario
        sy.proc_while_condition(lambda self: not self.estado_estacionario)
        
        # correr otras 1000.0 unidades de tiempo
        sy.proc_until(sy.time + 1000.0)
        
        sy.proc_while_condition(lambda self: len(self.q.clients.queue) <1)
        
        #if displaying:
        #    sy.dump()
        #    tp.sleep(0.1)


    # log
    sy.log()
    
    print
    print "STATISTICS"
    print

    print "time simulated:", sy.time
    print "estado estacionario:", sy.estado_estacionario
    
    def avg(v):
        return sum(v)/len(v)
        
    vW  = np.zeros(len(sy.history), dtype=float)
    vWq = np.zeros(len(sy.history), dtype=float)
    vWs = np.zeros(len(sy.history), dtype=float)
    for i in range(len(sy.history)):
        c = sy.history[i]
        vW[i]  = c.left - c.arrive
        vWq[i] = c.served - c.arrive
        vWs[i] = c.left - c.served
    eW = avg(vW)
    eWq = avg(vWq)
    eWs = avg(vWs)
    
    
    N = max(sy.counter) + 1
    P = np.zeros(N, dtype=float)
    for i in sy.counter:
        P[i] = sy.counter[i] / sy.time
    print "{:<6}   {:<10}   {:<8}".format("n", "Pn", "veces")
    for n in range(N):
        print ("{:<6}   {:0.8f}   {:<8}").format(n, P[n], sy.veces[n])
    
    
    eL = 0.0
    for i in range(len(P)):
        eL += P[i] * i
        
    Nq = max(sy.counter_q) + 1
    Pq = np.zeros(Nq, dtype=float)
    for i in sy.counter_q:
        Pq[i] = sy.counter_q[i] / sy.time
    eLq = 0.0
    for i in range(len(Pq)):
        eLq += Pq[i] * i
    
    aW, aWq, aWs, aLq, aL = 0.0, 0.0, 0.0, 0.0, 0.0
    
    if sy.q.lam >= sy.s_list[0].mu * len(sy.s_list):
        print "No se pueden calcular analiticamente"
    else:
        aW = W(sy.q.lam, sy.s_list[0].mu, len(sy.s_list))
        aWq = Wq(sy.q.lam, sy.s_list[0].mu, len(sy.s_list))
        aWs = aW - aWq
        aLq = Lq(sy.q.lam, sy.s_list[0].mu, len(sy.s_list))
        aL = L(sy.q.lam, sy.s_list[0].mu, len(sy.s_list))
    
    def difperc(a, b):
        if b == 0.0:
            return 0.0
        return 100.0 * (b - a)/b
    
    print
    print "    {:<12}  {:12}  {:12}".format("observado", "analizado", "diff")
    print "W   {:<12f}  {:<12f}  {:>+6.2f}%".format(eW, aW, difperc(eW, aW))
    print "Wq  {:<12f}  {:<12f}  {:>+6.2f}%".format(eWq, aWq, difperc(eWq, aWq))
    print "Ws  {:<12f}  {:<12f}  {:>+6.2f}%".format(eWs, aWs, difperc(eWs, aWs))
    print "Lq  {:<12f}  {:<12f}  {:>+6.2f}%".format(eLq, aLq, difperc(eLq, aLq))
    print "L   {:<12f}  {:<12f}  {:>+6.2f}%".format(eL, aL, difperc(eL, aL))
    print
            
main()
