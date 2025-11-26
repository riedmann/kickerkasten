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


class SevenSegmentGoals(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        
        print(f"[{datetime.now()}] SevenSegmentGoals.__init__() called!")
        print("Stack trace for initialization:")
        traceback.print_stack()
        sys.stdout.flush()
        
        # Create separate I2C instances for each segment to avoid conflicts
        i2c1 = busio.I2C(board.SCL, board.SDA)
        i2c2 = busio.I2C(board.SCL, board.SDA)
        
        self.segment1 = segments.Seg7x4(i2c1, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment2 = segments.Seg7x4(i2c2, address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        
        # Set brightness (0.0 to 1.0)
        self.segment1.brightness = 1.0
        self.segment2.brightness = 1.0
        
        # Disable auto_write and use manual show() to prevent conflicts
        self.segment1.auto_write = False
        self.segment2.auto_write = False
        
        # Store current values to detect changes
        self.current_goals1 = 0
        self.current_goals2 = 0
        self.needs_refresh = False
        
        print(f"[{datetime.now()}] Calling printToSegment(0,0) from __init__")
        self.printToSegment(0,0)
        
        # Start the refresh thread
        self.start()
    
    def run(self):
        """Background thread to periodically refresh the display"""
        while True:
            sleep(2)  # Check every 2 seconds
            if self.needs_refresh:
                self.refresh()
                self.needs_refresh = False
        

       
    def printToSegment(self, goals1, goals2):
        # Store the values
        self.current_goals1 = goals1
        self.current_goals2 = goals2
        self.needs_refresh = True  # Trigger periodic refresh
        
        # Format without leading zeros: "0:0", "1:0", "10:4"
        display_str = "{}{}".format(goals1, goals2)
        print(f"[{datetime.now()}] Updating goal display to: {goals1}:{goals2} (display_str: {display_str})")
        
        # Debug: Print stack trace if resetting to 0:0
        if goals1 == 0 and goals2 == 0:
            print(f"[{datetime.now()}] WARNING: Resetting display to 0:0!")
            print("Stack trace:")
            traceback.print_stack()
            sys.stdout.flush()
        
        self._write_to_display(display_str)
        
        print(f"[{datetime.now()}] Goal display updated successfully")
        sys.stdout.flush()
    
    def _write_to_display(self, display_str):
        """Internal method to actually write to the hardware"""
        # Use lock to prevent I2C bus contention
        with i2c_lock:
            try:
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
            except Exception as e:
                print(f"[{datetime.now()}] ERROR updating display: {e}")
                traceback.print_exc()
                sys.stdout.flush()
    
    def refresh(self):
        """Refresh the display with current values - call this if display gets corrupted"""
        print(f"[{datetime.now()}] Refreshing display to: {self.current_goals1}:{self.current_goals2}")
        display_str = "{}{}".format(self.current_goals1, self.current_goals2)
        self._write_to_display(display_str)
    
   