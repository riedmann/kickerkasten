"""
Score tracking and display handler
"""
from threading import Lock


class ScoreManager:
    """Manages score for both teams"""
    
    def __init__(self):
        self.lock = Lock()
        self.team_left = 0
        self.team_right = 0
    
    def goal_left(self):
        """Increment left team score"""
        with self.lock:
            self.team_left += 1
            return self.get_score()
    
    def goal_right(self):
        """Increment right team score"""
        with self.lock:
            self.team_right += 1
            return self.get_score()
    
    def reset(self):
        """Reset both scores to 0"""
        with self.lock:
            self.team_left = 0
            self.team_right = 0
            return self.get_score()
    
    def get_score(self):
        """Get current score"""
        with self.lock:
            return {
                "team_left": self.team_left,
                "team_right": self.team_right
            }
