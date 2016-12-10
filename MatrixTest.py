# Test Matrix16x16
from time import sleep
from random import randrange

from Matrix16x16 import Matrix16x16 as M16

PERCENT_FILL = 10

m = M16()
m.begin()

while True:
    m.clear()
    for i in xrange(int(2.56 * PERCENT_FILL)):
        x = randrange(0, 16)
        y = randrange(0, 16)
        m.set_pixel(x, y, 1)
    m.write_display()
    sleep(0.1)