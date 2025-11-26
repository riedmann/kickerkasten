"""
Sound manager for playing game sounds
"""
import pygame
import os
import config


class SoundManager:
    """Handles all game sounds"""
    
    def __init__(self):
        pygame.mixer.init()
        
        # Load sound files
        sound_path = os.path.join(os.path.dirname(__file__), '..', 'sound')
        
        self.goal_sound = pygame.mixer.Sound(os.path.join(sound_path, 'goal.ogg'))
        self.start_sound = pygame.mixer.Sound(os.path.join(sound_path, 'start.ogg'))
        self.nogoal_sound = pygame.mixer.Sound(os.path.join(sound_path, 'nogoal.ogg'))
        
        print("Sound manager initialized")
        print(f"  Sound folder: {sound_path}")
    
    def play_goal(self):
        """Play goal sound"""
        print("[SOUND] Playing goal sound")
        self.goal_sound.play()
    
    def play_start(self):
        """Play start/stop/pause sound"""
        print("[SOUND] Playing start sound")
        self.start_sound.play()
    
    def play_nogoal(self):
        """Play invalid goal sound"""
        print("[SOUND] Playing nogoal sound")
        self.nogoal_sound.play()
