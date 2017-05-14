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
from collections import deque
#import sqlite3

from lifedisplay import LifeDisplay

MIN_RATE        = 0.01  # fastest rate (secs)
MAX_RATE        = 1.00  # slowest   "    "
MIN_GENS        = 5     # minimum number of steps (generations)
MAX_GENS        = 500   # maximum   "    "    "         "
MIN_BRIGHTNESS  = 1     # minimum brightness setting
MAX_BRIGHTNESS  = 15    # maximum    "          "
PERCENT_FILL    = 50    # universe fill factor
MAX_HIST        = 20    # maximum history to track universe
MAX_CYCLES      = 20    # maximum cycles for oscillators
RATE_KNOB       = 0
GEN_KNOB        = 1
BRIGHTNESS_KNOB = 2
ALLOW_INFINITE  = True  # if True, max gen = infinite
SQLDB           = 'life_stats.db'

NX = 16
NY = 16

life_disp = LifeDisplay()

history = deque(maxlen=MAX_HIST)
cycle_count = 0

# create darkness
U = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
generation = 0
startID = 0

def read_gen_knob():
    """Return max generation value for current knob setting."""
    value = 1.0*life_disp.read_adc(GEN_KNOB)
    return int(MIN_GENS + (value/1023.0)*(MAX_GENS-MIN_GENS))

def read_rate_knob():
    """Return rate value for current knob setting."""
    value = 1.0*life_disp.read_adc(RATE_KNOB)
    return MIN_RATE + (value/1023.0)*(MAX_RATE-MIN_RATE)

def read_brightness_knob():
    """Return brightness value for current knob setting."""
    value = 1.0*life_disp.read_adc(BRIGHTNESS_KNOB)
    return MIN_BRIGHTNESS + int(round((value/1023.0)*(MAX_BRIGHTNESS-MIN_BRIGHTNESS)))

def knob_sleep():
    """Sleep, but also check knob while doing so."""
    start_wait = datetime.now()
    while (datetime.now() - start_wait).total_seconds() < read_rate_knob():
        pass  # the dutchie on the left hand side

def create_world(fill):
    """Let there be light."""
    UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
    for i in xrange(int(0.01 * NX * NY * fill)):
        x = randrange(1,NX+1)
        y = randrange(1,NY+1)
        UU[x][y] = 1
    return UU
        
def get_universe_id():
    """Return unique 2**256 bit integer value."""
    N = 0;
    ID = 0;
    for x in xrange(NX):
        for y in xrange(NY):
            ID += U[x+1][y+1]*(2**N)
            N += 1
    return ID

def display_universe():
    """Show it."""
    try:
        life_disp.set_brightness(read_brightness_knob())
        life_disp.clear()
        for x in xrange(NX):
            for y in xrange(NY):
                life_disp.set_pixel(x, y, U[x+1][y+1])
        life_disp.write_display()
    except IOError:
        print "I2C comm barf. But life goes on!"

def count_neighbors(x, y):
    """Return neighbor count."""
    return  U[x-1][y-1] + U[x][y-1] + U[x+1][y-1] + \
            U[x-1][y]   +             U[x+1][y]   + \
            U[x-1][y+1] + U[x][y+1] + U[x+1][y+1]

def update_universe():
    """Life goes on."""
    global generation
    generation += 1
    UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
    for x in xrange(1,NX+1):
        for y in xrange(1,NY+1):
            UU[x][y] = U[x][y]
            N = count_neighbors(x,y)
            if UU[x][y]:
                # live cell rules
                if N < 2 or N > 3:
                    UU[x][y] = 0
            else:
                # dead cell rules
                if N == 3:
                    UU[x][y] = 1
    return UU

def genesis():
    """Biblical kind. Not Phil Collins prog-rock kind."""
    global U, generation, cycle_count, startID
    history.clear()
    generation = 1
    cycle_count = 0
    U = create_world(PERCENT_FILL)
    startID = get_universe_id()
    history.appendleft(startID)
    display_universe()
    knob_sleep()

# Bootstrap a new universe
genesis()

while True:
    # Start over if max generations reached
    gen_knob = read_gen_knob()
    if not(ALLOW_INFINITE and gen_knob == MAX_GENS) and generation >= gen_knob:
        print "Universe lived long enough at generation {0}.".format(generation)
        genesis()

    # Update the universe per the rules of the game of life
    U = update_universe()
    
    # Check for still lifes and oscillators
    ID = get_universe_id()
    if history.count(ID):
        # Let it repeat for a few cycles
        cycle_count += 1
        if (cycle_count > MAX_CYCLES):
            p = 0
            if ID != 0:
                # Count period of oscillator                
                for h in history:
                    p += 1
                    if ID == h:
                        break
            print("Oscillator period {0} at generation {1}.").format(p,generation)
            
            # Store stats in database
            #store_stats(generation, p)
            
            # Start over
            genesis()
            
    # Update history after 1st gen
    if generation != 1:
        history.appendleft(ID)
    
    # Display the current universe
    display_universe()

    # Sleep
    knob_sleep()