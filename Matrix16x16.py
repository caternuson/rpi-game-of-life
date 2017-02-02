# Matrix 16x16
#
# A thing what has 2 Matrix16x8's

import Matrix16x8

class Matrix16x16():
    
    def __init__(self, address1=0x70, address2=0x71):
        self.m1 = Matrix16x8.Matrix16x8(address=address1)
        self.m2 = Matrix16x8.Matrix16x8(address=address2)
        
    def begin(self, ):
        self.m1.begin()
        self.m2.begin()
        
    def clear(self, ):
        self.m1.clear()
        self.m2.clear()
        
    def write_display(self, ):
        self.m1.write_display()
        self.m2.write_display()
        
    def set_pixel(self, x, y, value):
        if y < 8:
            self.m1.set_pixel(x, y, value)
        elif y < 16:
            self.m2.set_pixel(x, y-8, value)

    def set_brightness(self, brightness):
        self.m1.set_brightness(brightness)
        self.m2.set_brightness(brightness)
            
# skipping other functions for now
