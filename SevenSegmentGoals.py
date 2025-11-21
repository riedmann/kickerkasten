from threading import Thread
from time import sleep
import constant
import sys
import board
import busio
from adafruit_ht16k33 import segments
import traceback
from datetime import datetime
from i2c_lock import i2c_lock


class SevenSegmentGoals:
    def __init__(self):
        print(f"[{datetime.now()}] SevenSegmentGoals.__init__() called!")
        print("Stack trace for initialization:")
        traceback.print_stack()
        sys.stdout.flush()
        
        i2c = busio.I2C(board.SCL, board.SDA)
        self.segment1 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment2 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        
        # Set brightness (0.0 to 1.0)
        self.segment1.brightness = 1.0
        self.segment2.brightness = 1.0
        
        # Disable auto_write and use manual show() to prevent conflicts
        self.segment1.auto_write = False
        self.segment2.auto_write = False
        
        print(f"[{datetime.now()}] Calling printToSegment(0,0) from __init__")
        self.printToSegment(0,0)
        

       
    def printToSegment(self, goals1, goals2):
        # Format without leading zeros: "0:0", "1:0", "10:4"
        display_str = "{}{}".format(goals1, goals2)
        print(f"[{datetime.now()}] Updating goal display to: {goals1}:{goals2} (display_str: {display_str})")
        
        # Debug: Print stack trace if resetting to 0:0
        if goals1 == 0 and goals2 == 0:
            print(f"[{datetime.now()}] WARNING: Resetting display to 0:0!")
            print("Stack trace:")
            traceback.print_stack()
            sys.stdout.flush()
        
        # Use lock to prevent I2C bus contention
        with i2c_lock:
            # Update segment1
            self.segment1.fill(0)
            self.segment1.print(display_str)
            self.segment1.colon = True
            self.segment1.show()
            
            # Update segment2
            self.segment2.fill(0)
            self.segment2.print(display_str)
            self.segment2.colon = True
            self.segment2.show()
        
        print(f"[{datetime.now()}] Goal display updated successfully")
        sys.stdout.flush()
    
   