# Matrix 16x8
#
# because there isn't one yet?

from Adafruit_LED_Backpack import HT16K33

class Matrix16x8(HT16K33.HT16K33):
    
    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Matrix16x8, self).__init__(**kwargs)    

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 15.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > 15 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        self.set_led(y * 16 + x, value)
        
# skipping other functions for now