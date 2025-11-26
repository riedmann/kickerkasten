"""
GPIO handler for goal detection using gpiozero
"""
from gpiozero import Device, Button, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from . import config

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

        # Ball button and output
        self.ball_button = Button(
            config.GPIO_PIN_BALL_BUTTON,
            pull_up=False,
            bounce_time=bounce_time
        )
        self.ball_output = OutputDevice(config.GPIO_PIN_BALL_OUT, active_high=True, initial_value=False)

        self.ball_button.when_pressed = self._handle_ball_button
        
        # Register event handlers
        self.left_goal_button.when_pressed = self._handle_left_goal
        self.right_goal_button.when_pressed = self._handle_right_goal

        print(f"  Ball button: GPIO {config.GPIO_PIN_BALL_BUTTON}")
        print(f"  Ball out: GPIO {config.GPIO_PIN_BALL_OUT}")
        
        print("GPIO buttons initialized:")
        print(f"  Left goal: GPIO {config.GPIO_PIN_LEFT_GOAL}")
        print(f"  Right goal: GPIO {config.GPIO_PIN_RIGHT_GOAL}")
        print(f"  Bounce time: {bounce_time}s")
        print(f"  Pin factory: {Device.pin_factory}")
    
    def _handle_left_goal(self):
        """Internal handler for left goal button"""
        print(f"[GPIO] Left goal button pressed! (GPIO {config.GPIO_PIN_LEFT_GOAL})")
        if self.on_left_goal:
            try:
                self.on_left_goal()
                print("[GPIO] Left goal callback executed successfully")
            except Exception as e:
                print(f"[GPIO] Error in left goal callback: {e}")
        else:
            print("[GPIO] Warning: No callback registered for left goal")
    
    def _handle_right_goal(self):
        """Internal handler for right goal button"""
        print(f"[GPIO] Right goal button pressed! (GPIO {config.GPIO_PIN_RIGHT_GOAL})")
        if self.on_right_goal:
            try:
                self.on_right_goal()
                print("[GPIO] Right goal callback executed successfully")
            except Exception as e:
                print(f"[GPIO] Error in right goal callback: {e}")
        else:
            print("[GPIO] Warning: No callback registered for right goal")

    def _handle_ball_button(self):
        """Internal handler for ball button press: set output high, then low after short delay."""
        print(f"[GPIO] Ball button pressed! (GPIO {config.GPIO_PIN_BALL_BUTTON})")
        try:
            self.ball_output.on()
            from threading import Timer as ThreadingTimer
            ThreadingTimer(0.2, self.ball_output.off).start()  # 200ms pulse
            print("[GPIO] Ball output set HIGH, will reset LOW after 200ms")
        except Exception as e:
            print(f"[GPIO] Error in ball output logic: {e}")
