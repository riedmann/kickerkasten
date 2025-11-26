"""
Seven Segment Display Handler for Score
"""
from threading import Thread
from time import sleep
import board
import busio
from adafruit_ht16k33 import segments
from . import config
from .i2c_lock import i2c_lock


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
        """Background thread that refreshes display every 0.5 seconds"""
        while True:
            sleep(0.5)  # Refresh more frequently
            self._write_to_display()
    
    def update(self, team_left, team_right):
        """Update both displays with the score (left:right)"""
        self.team_left = team_left
        self.team_right = team_right
        self._write_to_display()
    
    def _write_to_display(self):
        """Internal method to write current score to displays"""
        try:
            with i2c_lock:
                # Update display 1 - positions are 0, 1, colon, 2, 3
                # Left score on positions 0-1, right score on positions 2-3
                self.display1.fill(0)
            
            # Left team score
            if self.team_left >= 10:
                self.display1[0] = str(self.team_left // 10)
                self.display1[1] = str(self.team_left % 10)
            else:
                self.display1[1] = str(self.team_left)
            
            # Right team score
            if self.team_right >= 10:
                self.display1[2] = str(self.team_right // 10)
                self.display1[3] = str(self.team_right % 10)
            else:
                self.display1[2] = str(self.team_right)
            
                self.display1.colon = True
                self.display1.show()
                
                # Update display 2 - mirror display 1
                self.display2.fill(0)
            
                # Left team score
                if self.team_left >= 10:
                    self.display2[0] = str(self.team_left // 10)
                    self.display2[1] = str(self.team_left % 10)
                else:
                    self.display2[1] = str(self.team_left)
                
                # Right team score
                if self.team_right >= 10:
                    self.display2[2] = str(self.team_right // 10)
                    self.display2[3] = str(self.team_right % 10)
                else:
                    self.display2[2] = str(self.team_right)
                
                self.display2.colon = True
                self.display2.show()
        except Exception as e:
            pass
    
    def clear(self):
        """Clear both displays"""
        with i2c_lock:
            self.display1.fill(0)
            self.display1.show()
            self.display2.fill(0)
            self.display2.show()
