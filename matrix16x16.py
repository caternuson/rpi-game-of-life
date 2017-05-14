#===============================================================================
# matrix16x16.py
#
# Class for interfacing to 16x16 LED matrix comprised of two Adafruit 8x16
# LED matrices.
#
# 16x16 LED Matrix Configuration
#
#       ---x   
#       |   +--------+
#       y   |  top   | m2
#        xx +--------+
#         Lyy
#           +--------+
#           |  bot   | m1
#        xx +--------+
#         Lyy
#
# 2017-04-30
# Carter Nelson
#===============================================================================
from Adafruit_LED_Backpack import Matrix8x16

class Matrix16x16():
    """Class for interfacing to 16x16 LED matrix comprised of two Adafruit 16x8
    LED matrices.
    """
    
    def __init__(self, bottom=0x70, top=0x71, brightness=15):
        self.m1 = Matrix8x16.Matrix8x16(address=bottom)
        self.m2 = Matrix8x16.Matrix8x16(address=top)
        
        self.m1.begin()
        self.m2.begin()
        
        self.m1.set_brightness(brightness)
        self.m2.set_brightness(brightness)
        
        self.m1.clear()
        self.m2.clear()
        
        self.m1.write_display()
        self.m2.write_display()
        
    def clear(self, ):
        self.m1.clear()
        self.m2.clear()
        
    def write_display(self, ):
        self.m1.write_display()
        self.m2.write_display()
        
    def set_pixel(self, x, y, value):
        xx = 15 - y
        yy = x
        if xx < 8:
            self.m1.set_pixel(xx, yy, value)
        else:
            self.m2.set_pixel(xx-8, yy, value)

    def set_brightness(self, brightness):
        self.m1.set_brightness(brightness)
        self.m2.set_brightness(brightness)
        
    def set_raw256(self, value):
        self.clear()
        for y in xrange(16):
            for x in xrange(16):
                self.set_pixel(15-x,15-y, value & 0x01)
                value >>= 1
        self.write_display()
        
    def bitmap2value(bmp):
        value = 0
        for row in bmp:
            for bit in row:
                value <<= 1
                value += bit
        return value
