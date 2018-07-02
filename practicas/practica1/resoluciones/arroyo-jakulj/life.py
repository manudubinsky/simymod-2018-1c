import time
import curses
import sys


w=27
Matrix = [[0 for x in range(w)] for y in range(w)]
Nueva = [[0 for x in range(w)] for y in range(w)]

def cargar_matrix(path):
    f = open(path)

    line = f.readline()
    while line != "":
        xy = line.split(",")
        x = int(xy[0])
        y = int(xy[1])
        if 1 <= x and x <= 25 and 1 <= y and y <= 25:
            Matrix[x][y] = 1
            line = f.readline()
        else:
            raise Exception("Error en el archivo de coordenadas")

    f.close()

def guardar_matrix(ruta):
    f = open(ruta, "w")

    for y in range(1,w-1):
        for x in range(1,w-1):
            if Matrix[x][y] == 1:
                f.write(str(x) + "," + str(y) + "\n")
    
    f.close()

def iterar():
    for y in range(1, w-1):
        for x in range(1, w-1):
            nuevoestado(x,y)
    for y in range(1, w-1):
        for x in range(1, w-1):
            Matrix[x][y]=Nueva[x][y]

def nuevoestado (x,y):
    contador = Matrix[x-1][y-1] + \
               Matrix[x][y-1] + \
               Matrix[x+1][y-1] + \
               Matrix[x-1][y] + \
               Matrix[x+1][y] + \
               Matrix[x-1][y+1] + \
               Matrix[x][y+1] + \
               Matrix[x+1][y+1]

    if Matrix[x][y]==1:
        vive(x,y,contador)
    else:
        Revive(x,y,contador)
        
def vive(x,y,contador):
    if contador == 2 or contador == 3:
        Nueva[x][y]= 1
    else:
        Nueva[x][y]= 0

def Revive(x,y,contador):
    if contador == 3:
        Nueva[x][y]= 1
    else:
        Nueva[x][y]= 0

def MostrarMarco(ventana):
    ventana.addch(0, 0, curses.ACS_ULCORNER)
    for x in range(1, w-1):
        ventana.addch(0, x, curses.ACS_HLINE)
    ventana.addch(0, w-1, curses.ACS_URCORNER)
    
    for y in range(1, w-1):
        ventana.addch(y, 0,   curses.ACS_VLINE)
        ventana.addch(y, w-1, curses.ACS_VLINE)
    
    ventana.addch(w-1, 0, curses.ACS_LLCORNER)
    for x in range(1, w-1):
        ventana.addch(w-1, x, curses.ACS_HLINE)
    ventana.addch(w-1, w-1, curses.ACS_LRCORNER)

    ventana.addstr(w,   0, "[b] Iniciar/parar iteraciones")
    ventana.addstr(w+1, 0, "[q] Salir")
    ventana.addstr(w+2, 0, "[CLICK] Cambiar estado de celda")
    ventana.addstr(w+3, 0, "[s] Guardar archivo")

def Mostrar(ventana):
    for y in range(1, w-1):
        for x in range(1, w-1):
            if Matrix[x][y] == 1:
                ventana.addstr(y,x," ",curses.A_REVERSE)
            else:
                ventana.addstr(y,x," ")

def clickeado(ventana):
    (id, x, y, z, bstate) = curses.getmouse()

    if (bstate & curses.BUTTON1_PRESSED) and \
        1 <= x and x <= 25 and 1 <= y and y <= 25:

        if Matrix[x][y] == 0:
            Matrix[x][y] = 1
        else:
            Matrix[x][y] = 0
            
        Mostrar(ventana)
        ventana.refresh()

def main(ventana):
    ventana.clear()
    curses.noecho()
    curses.cbreak()
    ventana.keypad(True)
    ventana.resize(30,30)
    ventana.nodelay(True)
    curses.mousemask(curses.BUTTON1_PRESSED)
    
    if len(sys.argv >= 2):
        cargar_matrix(sys.argv[1])
    
    MostrarMarco(ventana)
    Mostrar(ventana)
    ventana.refresh()
    
    iterando = False
    salir = False
    ultima_iteracion = 0
    while not salir:
        t = time.time()
        
        c = ventana.getch()
        if c == ord('q'):
            salir = True
        elif c == ord('b'):
            iterando = not iterando
        elif c == curses.KEY_MOUSE:
            clickeado(ventana)
        elif c == ord("s"):
            guardar("out.txt")
        
        if iterando and t > ultima_iteracion + 0.25:
            iterar()
            Mostrar(ventana)
            ventana.refresh()
            ultima_iteracion = t

curses.wrapper(main)
