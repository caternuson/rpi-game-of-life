#===============================================================================
# game_of_life_16x16.py
#
# Class for interfacing to Raspberry Pi with four Adafruit 8x8 LEDs attached.
#
# 2015-04-15
# Carter Nelson
#===============================================================================
from time import sleep
from random import randrange

from Matrix16x16 import Matrix16x16 as M16