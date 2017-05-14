#===============================================================================
# GOL.py
#
# A thread class to provide creating and running a version of...
# Conway's Game of Life on a 16x6 LED matrix.
#
# * Any live cell with fewer than two live neighbours dies (underpopulation)
# * Any live cell with two or three live neighbours lives
# * Any live cell with more than three live neighbours dies (overpopulation)
# * Any dead cell with exactly three live neighbours becomes a live cell (reproduction)
#
# 2017-04-11
# Carter Nelson
#===============================================================================
import threading
from time import sleep
from datetime import datetime
from random import randrange
from collections import deque

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

NX = 16
NY = 16

class GOL(threading.Thread):
    """Thread class for running Conway's Game of Life."""

    def __init__(self, uni=None, group=None, target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)

        self.display = LifeDisplay()
        self.history = deque(maxlen=MAX_HIST)
        self.max_cycles = MAX_CYCLES
        self.threadAlive = False
        self.running = False
        self.autoRestart = False
        if not uni==None:
            self.U = uni
        #self.genesis()

    def __read_gen_knob(self, ):
        """Return max generation value for current knob setting."""
        value = 1.0*self.display.read_adc(GEN_KNOB)
        return int(MIN_GENS + (value/1023.0)*(MAX_GENS-MIN_GENS))

    def __read_rate_knob(self, ):
        """Return rate value for current knob setting."""
        value = 1.0*self.display.read_adc(RATE_KNOB)
        return MIN_RATE + (value/1023.0)*(MAX_RATE-MIN_RATE)

    def __read_brightness_knob(self, ):
        """Return brightness value for current knob setting."""
        value = 1.0*self.display.read_adc(BRIGHTNESS_KNOB)
        return MIN_BRIGHTNESS + int(round((value/1023.0)*(MAX_BRIGHTNESS-MIN_BRIGHTNESS)))

    def __knob_sleep(self, ):
        """Sleep, but also check knob while doing so."""
        start_wait = datetime.now()
        while (datetime.now() - start_wait).total_seconds() < self.readRateKnob():
            pass  # the dutchie on the left hand side

    def __create_world(self, fill):
        """Let there be light."""
        UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
        for i in xrange(int(0.01 * NX * NY * fill)):
            x = randrange(1,NX+1)
            y = randrange(1,NY+1)
            UU[x][y] = 1
        return UU
        
    def __get_universe_id(self, ):
        """Return unique 2**256 bit integer value."""
        N = 0;
        ID = 0;
        for x in xrange(NX):
            for y in xrange(NY):
                ID += self.U[x+1][y+1]*(2**N)
                N += 1
        return ID

    def __display_universe(self, ):
        """Show it."""
        try:
            self.display.set_brightness(self.readBrightnessKnob())
            self.display.clear()
            for x in xrange(NX):
                for y in xrange(NY):
                    self.display.set_pixel(x, y, self.U[x+1][y+1])
            self.display.write_display()
        except IOError:
            #print "I2C comm barf. But life goes on!"
            pass

    def __count_neighbors(self, x, y):
        """Return neighbor count."""
        return  self.U[x-1][y-1] + self.U[x][y-1] + self.U[x+1][y-1] + \
                self.U[x-1][y]   +             self.U[x+1][y]   + \
                self.U[x-1][y+1] + self.U[x][y+1] + self.U[x+1][y+1]

    def __update_universe(self, ):
        """Life goes on."""
        #global generation
        self.generation += 1
        UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
        for x in xrange(1,NX+1):
            for y in xrange(1,NY+1):
                UU[x][y] = self.U[x][y]
                N = self.countNeighbors(x,y)
                if UU[x][y]:
                    # live cell rules
                    if N < 2 or N > 3:
                        UU[x][y] = 0
                else:
                    # dead cell rules
                    if N == 3:
                        UU[x][y] = 1
        return UU
      
    def __add_uni_border(self, uni):
        """Expand 16x16 uni to 18x18 by adding single border of cells."""
        UU = [[0 for x in xrange(NX+2)] for y in xrange(NY+2)]
        for x in xrange(1,NX+1):
            for y in xrange(1,NY+1):
                UU[x][y] = uni[x-1][y-1]
        return UU

    def __genesis(self, uni=None):
        """Biblical kind. Not Phil Collins prog-rock kind."""
        self.history.clear()
        self.generation = 1
        self.cycle_count = 0
        if uni==None:
            self.U = self.createWorld(PERCENT_FILL)
        else:
            self.U = self.addUniBorder(uni)
        self.history.appendleft(self.getUniverseID())

    def set_universe(self, uni):
        """Run provided 16x16 Universe."""
        if not self.threadAlive:
            return
        if self.running:
            self.running = False
        self.genesis(uni)
        self.running = True

    def pause(self, ):
        """Pause thread main loop."""
        self.running = False
    
    def restart(self, ):
        """Restart thread main loop."""
        self.running = True
        
    def kill(self, ):
        """Kill thread."""
        self.threadAlive = False
        self.running = False

    def run(self, ):
        """Don't call directly. Called when thread is started."""
        self.threadAlive = True
        self.running = True
        
        while self.threadAlive:
            while self.running:
              # Start over if max generations reached
              genKnob = self.readGenKnob()
              if not(ALLOW_INFINITE and genKnob == MAX_GENS) and self.generation >= genKnob:
                  #print "Universe lived long enough at generation {0}.".format(self.generation)
                  #self.genesis()
                  pass
          
              # Update the universe per the rules of the game of life
              self.U = self.updateUniverse()
              
              # Check for still lifes and oscillators
              ID = self.getUniverseID()
              if self.history.count(ID):
                  # Let it repeat for a few cycles
                  self.cycle_count += 1
                  if not self.max_cycles == 0 and self.cycle_count > self.max_cycles:
                      p = 0
                      if ID != 0:
                          # Count period of oscillator                
                          for h in self.history:
                              p += 1
                              if ID == h:
                                  break
                      #print("Oscillator period {0} at generation {1}.").format(p,self.generation)
                      
                      # Store stats in database
                      #store_stats(generation, p)
                      
                      # Start over
                      if self.autoRestart:
                        self.genesis()
                      else:
                        self.running = False
                        continue
                      
              # Update history after 1st gen
              if self.generation != 1:
                  self.history.appendleft(ID)
              
              # Display the current universe
              self.displayUniverse()
          
              # Sleep
              self.knobSleep()