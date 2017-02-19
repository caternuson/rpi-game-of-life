#===============================================================================
# rpi_life_display.py
#
# Class for interfacing to Raspberry Pi with 16x16 LED Matrix and ADC attached
# to potentiometers.
#
# 16x16 LED Matrix Configuration
#
#       ---x   
#       |   +--------+
#       y   |  0x71  | m2
#        xx +--------+
#         Lyy
#           +--------+
#           |  0x70  | m1
#        xx +--------+
#         Lyy
#
# 2017-02-18
# Carter Nelson
#===============================================================================
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from Adafruit_LED_Backpack import Matrix8x16

class RpiLifeDisplay():
    """Class for interfacing to Raspberry Pi with 16x16 LED Matrix and
       ADC attached to potentiometers."""
    
    def __init__(self, brightness=15):
        self.m1 = Matrix8x16.Matrix8x16(address=0x70)
        self.m2 = Matrix8x16.Matrix8x16(address=0x71)
        
        self.m1.begin()
        self.m2.begin()
        
        self.m1.set_brightness(brightness)
        self.m2.set_brightness(brightness)
        
        self.m1.clear()
        self.m2.clear()
        
        self.m1.write_display()
        self.m2.write_display()
        
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

    #---------------------------------------------------------------
    #                         M A T R I X
    #---------------------------------------------------------------
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

    #---------------------------------------------------------------
    #                            A D C
    #---------------------------------------------------------------
    def get_raw_knobs(self, ):
        """Return the raw ADC values of the 3 knobs."""
        return (self.mcp.read_adc(0),
                self.mcp.read_adc(1),
                self.mcp.read_adc(2))
    
    def read_adc(self, chan):
        """Return the raw ADC value for the given channel."""
        return self.mcp.read_adc(chan)