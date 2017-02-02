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
from datetime import datetime
from random import randrange

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from Matrix16x16 import Matrix16x16 as M16

MIN_RATE        = 0.01  # fastest rate (secs)
MAX_RATE        = 1.00  # slowest   "    "
MIN_GENS        = 5     # minimum number of steps (generations)
MAX_GENS        = 500   # maximum   "    "    "         "
PERCENT_FILL    = 50    # universe fill factor
RATE_KNOB       = 0
GEN_KNOB        = 1

NX = 16
NY = 16

m = M16()
m.begin()
m.set_brightness(15)
m.clear()

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

# create darkness
U = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
generation = 0

def getKnobs():
    """Return the raw ADC values of the 3 knobs."""
    return (mcp.read_adc(0),mcp.read_adc(1),mcp.read_adc(2))

def readGenKnob():
    value = 1.0*mcp.read_adc(GEN_KNOB)
    return int(MIN_GENS + (value/1024.0)*(MAX_GENS-MIN_GENS))

def readRateKnob():
    value = 1.0*mcp.read_adc(RATE_KNOB)
    return MIN_RATE + (value/1024.0)*(MAX_RATE-MIN_RATE)

def knobSleep():
    start_wait = datetime.now()
    while (datetime.now() - start_wait).total_seconds() < readRateKnob():
            pass

def createWorld(fill):
    """Let there be light."""
    global U, generation
    generation = 0
    for i in xrange(int(0.01 * NX * NY * fill)):
        x = randrange(1,NX+1)
        y = randrange(1,NY+1)
        U[x][y] = 1

def displayUniverse():
    """Show it."""
    m.clear()
    for x in xrange(NX):
        for y in xrange(NY):
            m.set_pixel(x, y, U[x+1][y+1])
    m.write_display()

def countNeighbors(x, y):
    """Return neighbor count."""
    return  U[x-1][y-1] + U[x][y-1] + U[x+1][y-1] + \
            U[x-1][y]   +             U[x+1][y]   + \
            U[x-1][y+1] + U[x][y+1] + U[x+1][y+1]

def updateUniverse():
    """Life goes on."""
    global generation
    generation += 1
    UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
    for x in xrange(1,NX+1):
        for y in xrange(1,NY+1):
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

# Bootstrap a new universe
createWorld(PERCENT_FILL)
displayUniverse()
knobSleep()

while True:
    # Update the universe per the rules of the game of life
    U = updateUniverse()
    
    # Start over if universe is dead (no live cells)
    if not sum(row.count(1) for row in U):
        print "Universe died at generation {0}.".format(generation)
        createWorld(PERCENT_FILL)
        
    # Start over if max generations reached
    if generation >= readGenKnob():
        print "Universe lived long enough at generation {0}.".format(generation)
        createWorld(PERCENT_FILL)
        
    # Display the current universe
    displayUniverse()
    
    # Sleep
    knobSleep()