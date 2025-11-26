from threading import Thread, current_thread
from .LedAnimation import LedAnimation
import RPi.GPIO as GPIO
import Adafruit_WS2801 as LED
import Adafruit_GPIO.SPI as SPI
import random

class LedHandler:
    def __init__(self, pixel_count=160, spi_port=0, spi_device=0):
        print("Starting LedHandler...")
        self.PIXEL_COUNT = pixel_count
        self.pixels = LED.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(spi_port, spi_device), gpio=GPIO)
        self.current_animation = None
        self.current_thread = None
        self.loop_animation_id = None
        self.timer = None
        
        # Start with pause mode animation (case_1)
        self.runLed(1, loop=True)
    
    def set_timer(self, timer):
        """Set reference to timer to check game state"""
        self.timer = timer
    
    def switch_to_pause_mode(self):
        """Switch to pause animation (case_1)"""
        self.runLed(1, loop=True)
    
    def switch_to_game_mode(self):
        """Switch to active game animation (random 2-9)"""
        animation_id = random.randint(2, 9)
        self.runLed(animation_id, loop=True)
    
    def start_random_animation(self):
        """Start a random animation from 2-9"""
        animation_id = random.randint(2, 9)
        self.runLed(animation_id, loop=True)

    def runLed(self, animationID, loop=True, from_internal=False):
        """Start an LED animation, stopping any current animation"""
        print(f"Starting animation {animationID} (loop={loop})")
        
        # Stop current animation if running
        if self.current_animation:
            self.current_animation.stop()
            # Only join if we're not being called from the animation thread itself
            if self.current_thread and not from_internal and self.current_thread != current_thread():
                self.current_thread.join(timeout=1.0)
        
        # Create new animation
        self.current_animation = LedAnimation(self.pixels)
        
        # Store loop animation ID for later restoration
        if loop:
            self.loop_animation_id = animationID
        
        # Start animation thread
        self.current_thread = Thread(target=self._run_animation, args=(animationID, loop))
        self.current_thread.start()
    
    def _run_animation(self, animationID, loop):
        """Internal method to run animation and restore loop if needed"""
        self.current_animation.printLED(animationID, loop=loop)
        
        # If this was a one-time animation (like goal), restart the loop animation
        if not loop and self.loop_animation_id:
            print(f"Restoring loop animation {self.loop_animation_id}")
            self.runLed(self.loop_animation_id, loop=True, from_internal=True)
