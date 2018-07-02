import random
import curses
import time
import configparser

def comparision(a,b,w, matriz):
    if (a >= 0 and a < w) and (b >= 0 and b < w):
        if matriz[a][b] == 1:
            return 1
    return 0

def drawMatriz(stdscr, matriz, w):
    z = ''
    for x in range(w):
        for y in range(w):
            if matriz[x][y] == 0:
                z = ' '
            elif matriz[x][y] == 1:
                z = 'X'
            stdscr.addstr(x, y, z)
            stdscr.refresh()

def drawMenuBar(stdscr, cursor_x, cursor_y, height,width):
    statusbarstr = "Presione 'b' para iniciar | Presione 'q' para salir | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 1, 0, statusbarstr)
    stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

def config():
    cfg = configparser.ConfigParser()
    cfg.read('juego.cfg')
    if 'General' in cfg:
        general = cfg['General']
        w = general.get('filas')
        h = general.get('columnas')
        return w,h

def main(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    contViva = 0
    w = 0
    h = 0

    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    init = config()
    w = int(init[0])
    h = int(init[1])

    matriz = [[0 for x in range(w)] for y in range(h)]
    matriz2 = [[0 for x in range(w)] for y in range(h)]
    readFile("./naves", matriz)

    drawMatriz(stdscr, matriz, w)
    drawMenuBar(stdscr, cursor_x, cursor_y, height, width)

    k = stdscr.getch()
    stdscr.nodelay(1)
    while (k != ord('q') or (k == ord('b'))):
        for x in range(w):
            for y in range(w):
                contViva += comparision(x - 1, y - 1, w, matriz)
                contViva += comparision(x - 1, y, w, matriz)
                contViva += comparision(x - 1, y + 1, w, matriz)
                contViva += comparision(x, y - 1, w, matriz)
                contViva += comparision(x, y + 1, w, matriz)
                contViva += comparision(x + 1, y - 1, w, matriz)
                contViva += comparision(x + 1, y, w, matriz)
                contViva += comparision(x + 1, y + 1, w, matriz)

                if matriz[x][y] == 0:
                    if contViva == 3:
                        matriz2[x][y] = 1
                    else:
                        matriz2[x][y] = 0
                elif matriz[x][y] == 1:
                    if contViva == 2 or contViva == 3:
                        matriz2[x][y] = 1
                    else:
                        matriz2[x][y] = 0
                contViva = 0

        drawMatriz(stdscr, matriz2, w)
        time.sleep(0.2)

        for x in range(w):
            for y in range(w):
                matriz[x][y] = matriz2[x][y]
        matriz2 = [[0 for x in range(w)] for y in range(h)]

        drawMenuBar(stdscr, cursor_x, cursor_y, height, width)
        k = stdscr.getch()

def readFile(ruta, matriz):
    file = open(ruta, "r")
    fileLines = file.readlines()
    for line in fileLines:
        positions = line.split(",")
        matriz[int(positions[0])][int(positions[1])] = 1

if __name__ == '__main__':
    curses.wrapper(main)
