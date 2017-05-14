#===============================================================================
# rpi_life_display.py
#
# Class for interfacing to Raspberry Pi with 16x16 LED Matrix and ADC attached
# to potentiometers.
#
# 16x16 LED Matrix Configuration
#
#       ---x   
#       | +--------+
#       y |        |
#         |        |
#         |        |
#         +--------+
#
# 2017-02-18
# Carter Nelson
#===============================================================================
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matrix16x16

class LifeDisplay():
    """Class for interfacing to Raspberry Pi with 16x16 LED Matrix and
       ADC attached to potentiometers."""
    
    def __init__(self, brightness=15):
        self.disp = matrix16x16.Matrix16x16(brightness=brightness)
        
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

    #---------------------------------------------------------------
    #                         M A T R I X
    #---------------------------------------------------------------
    def clear(self, ):
        self.disp.clear()
        
    def write_display(self, ):
        self.disp.write_display()
        
    def set_pixel(self, x, y, value):
        self.disp.set_pixel(x, y, value)

    def set_brightness(self, brightness):
        self.disp.set_brightness(brightness)

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