"""
Sound manager for playing game sounds
"""
import os
from . import config
import simpleaudio as sa


class SoundManager:
    """Handles all game sounds"""
    
    def __init__(self):
        
        # Load sound files from config
        sound_path = config.SOUND_FOLDER
        self.goal_sound = os.path.join(sound_path, 'goal.wav')
        self.start_sound = os.path.join(sound_path, 'start.wav')
        self.nogoal_sound = os.path.join(sound_path, 'nogoal.wav')
        
        print("Sound manager initialized")
        print(f"  Sound folder: {sound_path}")
    
    def play_goal(self):
        """Play goal sound"""
        print("[SOUND] Playing goal sound")
        try:
            wave_obj = sa.WaveObject.from_wave_file(self.goal_sound)
            wave_obj.play()
        except Exception as e:
            print(f"[SOUND] Error playing goal sound: {e}")
    
    def play_start(self):
        """Play start/stop/pause sound"""
        print("[SOUND] Playing start sound")
        try:
            wave_obj = sa.WaveObject.from_wave_file(self.start_sound)
            wave_obj.play()
        except Exception as e:
            print(f"[SOUND] Error playing start sound: {e}")
    
    def play_nogoal(self):
        """Play invalid goal sound"""
        print("[SOUND] Playing nogoal sound")
        try:
            wave_obj = sa.WaveObject.from_wave_file(self.nogoal_sound)
            wave_obj.play()
        except Exception as e:
            print(f"[SOUND] Error playing nogoal sound: {e}")
