"""
Seven Segment Display Handler for Score
"""
from threading import Thread
from time import sleep
import board
import busio
from adafruit_ht16k33 import segments
import config
from i2c_lock import i2c_lock


class ScoreDisplay(Thread):
    """Handles two seven-segment displays for the score with auto-refresh"""
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        
        # Store current score
        self.team_left = 0
        self.team_right = 0
        
        # Create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Initialize both score displays with CORRECT addresses
        self.display1 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.display2 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        
        # Configure displays
        self.display1.brightness = 1.0
        self.display2.brightness = 1.0
        self.display1.auto_write = False
        self.display2.auto_write = False
        
        # Show initial score
        self._write_to_display()
        
        # Start refresh thread
        self.start()
    
    def run(self):
        """Background thread that refreshes display every 2 seconds"""
        while True:
            sleep(2)
            self._write_to_display()
    
    def update(self, team_left, team_right):
        """Update both displays with the score (left:right)"""
        self.team_left = team_left
        self.team_right = team_right
        print(f"[SCORE_DISPLAY] Score updated to {team_left}:{team_right}")
        self._write_to_display()
    
    def _write_to_display(self):
        """Internal method to write current score to displays"""
        # Format: "L:R" without leading zeros for single digits
        display_str = "{}{}".format(self.team_left, self.team_right)
        
        with i2c_lock:
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
            except Exception as e:
                print(f"[SCORE_DISPLAY] ERROR: {e}")
    
    def clear(self):
        """Clear both displays"""
        with i2c_lock:
            self.display1.fill(0)
            self.display1.show()
            self.display2.fill(0)
            self.display2.show()
