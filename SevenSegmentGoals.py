from threading import Thread
from time import sleep
import constant
import sys
import board
import busio
from adafruit_ht16k33 import segments


class SevenSegmentGoals:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.segment1 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment2 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        
        # Set brightness (0.0 to 1.0)
        self.segment1.brightness = 1.0
        self.segment2.brightness = 1.0
        
        # Enable auto_write for immediate display updates
        self.segment1.auto_write = True
        self.segment2.auto_write = True
        
        self.printToSegment(0,0)
        

       
    def printToSegment(self, goals1, goals2):
        # Format the display string for segment1
        display_str = "{:2d}{:2d}".format(goals1, goals2)
        print(f"Updating goal display to: {goals1}:{goals2} (display_str: {display_str})")
        
        # Clear and update segment1
        self.segment1.fill(0)
        self.segment1.print(display_str)
        self.segment1.colon = True
        self.segment1.show()
        
        # Clear and update segment2
        self.segment2.fill(0)
        self.segment2.print(display_str)
        self.segment2.colon = True
        self.segment2.show()
        
        print("Goal display updated successfully")
    
   