"""
Seven Segment Display Handler for Timer
"""
import board
import busio
from adafruit_ht16k33 import segments
from . import config
from .i2c_lock import i2c_lock


class TimerDisplay:
    """Handles two seven-segment displays for the timer"""
    
    def __init__(self):
        # Create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Initialize both timer displays
        self.display1 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_TIMER_1)
        self.display2 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_TIMER_2)
        
        # Configure displays
        self.display1.brightness = 1.0
        self.display2.brightness = 1.0
        self.display1.auto_write = False
        self.display2.auto_write = False
        
        # Show initial time
        self.update(config.DEFAULT_TIME_TO_RUN)
    
    def update(self, seconds):
        """Update both displays with the given time in seconds"""
        mins, secs = divmod(seconds, 60)
        display_str = "{:02d}{:02d}".format(mins, secs)
        
        if i2c_lock.acquire(timeout=2.0):
            try:
                # Update display 1
                self.display1.fill(0)
                self.display1.print(display_str)
                self.display1.colon = True
                self.display1.show()
                
                # Update display 2
                self.display2.fill(0)
                self.display2.print(display_str)
                self.display2.colon = True
                self.display2.show()
            finally:
                i2c_lock.release()
    
    def clear(self):
        """Clear both displays"""
        if i2c_lock.acquire(timeout=2.0):
            try:
                self.display1.fill(0)
                self.display1.show()
                self.display2.fill(0)
                self.display2.show()
            finally:
                i2c_lock.release()
