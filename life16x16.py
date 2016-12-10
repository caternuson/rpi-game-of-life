#===============================================================================
# life16x16.py
#
# Conway's Game of Life on a 16x6 LED matrix.
#
# * Any live cell with fewer than two live neighbours dies (underpopulation)
# * Any live cell with two or three live neighbours lives
# * Any live cell with more than three live neighbours dies (overpopulation)
# * Any dead cell with exactly three live neighbours becomes a live cell (reproduction)
#
# 2016-12-09
# Carter Nelson
#===============================================================================
from time import sleep
from random import randrange

from Matrix16x16 import Matrix16x16 as M16

UPDATE_RATE   = 1   # seconds
PERCENT_FILL  = 50  # universe fill
NX = 16
NY = 16

m = M16()
m.begin()
m.clear()

# create darkness
U = [[0 for x in xrange(NX)] for y in xrange(NY)]

def createWorld(fill):
    """Let there be light."""
    global U
    for i in xrange(int(0.01 * NX * NY * fill)):
        x = randrange(NX)
        y = randrange(NY)
        U[x][y] = 1

def displayUniverse():
    """Show it."""
    m.clear()
    for x in xrange(NX):
        for y in xrange(NY):
            m.set_pixel(x, y, U[x][y])
    m.write_display()

def countNeighbors(x, y):
    """Return neighbor count."""
    return  U[x-1][y-1] + U[x][y-1] + U[x+1][y-1] + \
            U[x-1][y]   +             U[x+1][y]   + \
            U[x-1][y+1] + U[x][y+1] + U[x+1][y+1]

def updateUniverse():
    """Life goes on."""
    UU = [[0 for x in xrange(NX)] for y in xrange(NY)]
    for x in xrange(1,NX-2):
        for y in xrange(1,NY-2):
            UU[x][y] = U[x][y]
            N = countNeighbors(x,y)
            if UU[x][y]:
                # live cell rules
                if N < 2 or N > 3:
                    UU[x][y] = 0
            else:
                # dead cell rules
                if N == 3:
                    UU[x][y] = 1
    return UU

createWorld(PERCENT_FILL)
displayUniverse()
sleep(UPDATE_RATE)

while True:
    U = updateUniverse()
    displayUniverse()
    if not sum(row.count(1) for row in U):
        exit('Universe died.')
    sleep(UPDATE_RATE)