"""
Timer class to handle countdown functionality
"""
from threading import Thread, Lock
from time import sleep
from . import config


class Timer(Thread):
    """Thread-safe timer with start, stop, pause, and reset functionality"""
    
    def __init__(self, display=None):
        Thread.__init__(self)
        self.daemon = True
        
        self.time_remaining = config.DEFAULT_TIME_TO_RUN
        self.is_running = False
        self.is_paused = True
        self.lock = Lock()
        self.display = display
        
    def run(self):
        """Main timer loop"""
        while True:
            sleep(1)
            
            should_update = False
            current_time = 0
            
            with self.lock:
                if self.is_running and not self.is_paused and self.time_remaining > 0:
                    self.time_remaining -= 1
                    should_update = True
                    current_time = self.time_remaining
                    
                    if self.time_remaining == 0:
                        self.is_running = False
                        self.is_paused = True
            
            # Update display outside the lock
            if should_update and self.display:
                self.display.update(current_time)
    
    def start_timer(self):
        """Start or resume the timer"""
        with self.lock:
            self.is_running = True
            self.is_paused = False
            return {
                "status": "started",
                "time_remaining": self.time_remaining,
                "is_paused": self.is_paused
            }
    
    def stop_timer(self):
        """Stop the timer completely"""
        with self.lock:
            self.is_running = False
            self.is_paused = True
            return {
                "status": "stopped",
                "time_remaining": self.time_remaining,
                "is_paused": self.is_paused
            }
    
    def pause_timer(self):
        """Pause the timer without resetting"""
        with self.lock:
            self.is_paused = True
            return {
                "status": "paused",
                "time_remaining": self.time_remaining,
                "is_paused": self.is_paused
            }
    
    def reset_timer(self, time_seconds=None):
        """Reset the timer to specified time or default"""
        print("in timer reset")
        with self.lock:
            print("in timer lock")
            if time_seconds is not None:
                self.time_remaining = time_seconds
            else:
                self.time_remaining = config.DEFAULT_TIME_TO_RUN
            
            self.is_running = False
            self.is_paused = True
            
            result = {
                "status": "reset",
                "time_remaining": self.time_remaining,
                "is_paused": self.is_paused
            }
        
        # Update display AFTER releasing the lock to avoid potential deadlock
        if self.display:
            self.display.update(self.time_remaining)
        
        return result
    
    def get_status(self):
        """Get current timer status"""
        with self.lock:
            mins, secs = divmod(self.time_remaining, 60)
            return {
                "time_remaining": self.time_remaining,
                "time_formatted": f"{mins:02d}:{secs:02d}",
                "is_running": self.is_running,
                "is_paused": self.is_paused
            }
