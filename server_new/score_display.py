"""
Seven Segment Display Handler for Score
"""
from threading import Lock
import board
import busio
from adafruit_ht16k33 import segments
import config


class ScoreDisplay:
    """Handles two seven-segment displays for the score"""
    
    def __init__(self):
        self.lock = Lock()
        
        # Create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Initialize both score displays
        self.display1 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        self.display2 = segments.Seg7x4(i2c, address=config.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        
        # Configure displays
        self.display1.brightness = 1.0
        self.display2.brightness = 1.0
        self.display1.auto_write = False
        self.display2.auto_write = False
        
        # Show initial score
        self.update(0, 0)
    
    def update(self, team_left, team_right):
        """Update both displays with the score (left:right)"""
        # Format: "L:R" without leading zeros for single digits
        display_str = "{}{}".format(team_left, team_right)
        
        print(f"[SCORE_DISPLAY] Acquiring lock to update to {team_left}:{team_right}")
        
        if self.lock.acquire(timeout=2):
            try:
                print(f"[SCORE_DISPLAY] Lock acquired, updating displays")
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
                
                print(f"[SCORE_DISPLAY] Displays updated successfully")
            except Exception as e:
                print(f"[SCORE_DISPLAY] ERROR updating displays: {e}")
                import traceback
                traceback.print_exc()
            finally:
                self.lock.release()
                print(f"[SCORE_DISPLAY] Lock released")
        else:
            print(f"[SCORE_DISPLAY] ERROR: Could not acquire lock after 2 seconds!")
    
    def clear(self):
        """Clear both displays"""
        with self.lock:
            self.display1.fill(0)
            self.display1.show()
            self.display2.fill(0)
            self.display2.show()
