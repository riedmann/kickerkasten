"""
GPIO handler for goal detection using gpiozero
"""
from gpiozero import Device, Button
from gpiozero.pins.lgpio import LGPIOFactory
import config

# Set the pin factory explicitly to use lgpio backend
Device.pin_factory = LGPIOFactory()


class GPIOHandler:
    """Handles GPIO button inputs for goal detection"""
    
    def __init__(self, on_left_goal=None, on_right_goal=None):
        """
        Initialize GPIO handler
        
        Args:
            on_left_goal: Callback function when left goal is scored
            on_right_goal: Callback function when right goal is scored
        """
        self.on_left_goal = on_left_goal
        self.on_right_goal = on_right_goal
        
        # Convert milliseconds to seconds for bounce time
        bounce_time = config.BOUNCETIME / 1000.0
        
        # Setup buttons with pull-down resistors
        self.left_goal_button = Button(
            config.GPIO_PIN_LEFT_GOAL, 
            pull_up=False, 
            bounce_time=bounce_time
        )
        self.right_goal_button = Button(
            config.GPIO_PIN_RIGHT_GOAL, 
            pull_up=False, 
            bounce_time=bounce_time
        )
        
        # Register event handlers
        self.left_goal_button.when_pressed = self._handle_left_goal
        self.right_goal_button.when_pressed = self._handle_right_goal
        
        print("GPIO buttons initialized:")
        print(f"  Left goal: GPIO {config.GPIO_PIN_LEFT_GOAL}")
        print(f"  Right goal: GPIO {config.GPIO_PIN_RIGHT_GOAL}")
        print(f"  Bounce time: {bounce_time}s")
        print(f"  Pin factory: {Device.pin_factory}")
    
    def _handle_left_goal(self):
        """Internal handler for left goal button"""
        print("Left goal scored!")
        if self.on_left_goal:
            self.on_left_goal()
    
    def _handle_right_goal(self):
        """Internal handler for right goal button"""
        print("Right goal scored!")
        if self.on_right_goal:
            self.on_right_goal()
