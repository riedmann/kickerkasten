import time
import Adafruit_WS2801 as LED
import threading

class LedAnimation:
    def __init__(self, pixels):
        self.pixels = pixels
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!
        self.should_stop = threading.Event()

    def printLED(self, animationId, loop=True):
        """Run animation, looping continuously unless loop=False"""
        while not self.should_stop.is_set():
            getattr(self, 'case_' + str(animationId), lambda: 'nothing')()
            if not loop:
                break
        self.pixels.clear()
        self.pixels.show()
    
    def stop(self):
        """Stop the current animation"""
        self.should_stop.set()

    # Define the wheel function to interpolate between different hues.
    def wheel(self,pos):
        if pos < 85:
            return LED.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return LED.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return LED.RGB_to_color(0, pos * 3, 255 - pos * 3)

    # Simple single point moving around - dim white/blue
    def case_1(self):
        pixels = self.pixels
        color = LED.RGB_to_color(30, 30, 50)  # Dim white-blue
        wait = 0.02
        
        for i in range(pixels.count()):
            if self.should_stop.is_set():
                break
            pixels.clear()
            pixels.set_pixel(i, color)
            pixels.show()
            time.sleep(wait)
                
    # appear from back
    def case_2(self):
        pixels = self.pixels
        color=(255, 0, 0)
        pos = 0
        #pixels.clear()
        for i in range(pixels.count()):
            for j in reversed(range(i, pixels.count())):
                pixels.clear()
                # first set all pixels at the begin
                for k in range(i):
                    pixels.set_pixel(k, LED.RGB_to_color( color[0], color[1], color[2] ))
                # set then the pixel at position j
                pixels.set_pixel(j, LED.RGB_to_color( color[0], color[1], color[2] ))
                pixels.show()
                time.sleep(0.03)
        #time.sleep(3)

    # rainbow_cycle
    def case_3(self):
        pixels = self.pixels
        wait=0.005
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in range(pixels.count()):
                pixels.set_pixel(i, self.wheel(((i * 256 // pixels.count()) + j) % 256) )
            pixels.show()
            if wait > 0:
                time.sleep(wait)
    
    # rainbow_colors
    def case_4(self):
        pixels = self.pixels
        wait=0.01
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in range(pixels.count()):
                pixels.set_pixel(i, self.wheel(((256 // pixels.count() + j)) % 256) )
            pixels.show()
            if wait > 0:
                time.sleep(wait)

    # brightness_decrease
    def case_5(self):     
        pixels = self.pixels
        wait=0.01
        step=1
        for j in range(int(256 // step)):
            for i in range(pixels.count()):
                r, g, b = pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                pixels.set_pixel(i, LED.RGB_to_color( r, g, b ))
            pixels.show()
            if wait > 0:
                time.sleep(wait)
     
    # blink color Red
    def case_6(self, blink_times=5, wait=0.5, color=(255,0,0)):
        pixels = self.pixels
        for i in range(blink_times):
            # blink two times, then wait
            pixels.clear()
            for j in range(2):
                for k in range(pixels.count()):
                    pixels.set_pixel(k, LED.RGB_to_color( color[0], color[1], color[2] ))
                pixels.show()
                time.sleep(0.08)
                pixels.clear()
                pixels.show()
                time.sleep(0.08)
            time.sleep(wait)
            
    def case_7(self):
        for i in range(1):
            self.case_6(blink_times = 1, color=(255, 0, 0))
            self.case_6(blink_times = 1, color=(0, 255, 0))
            self.case_6(blink_times = 1, color=(0, 0, 255))
                
    def case_8(self):
        pixels = self.pixels
        step=2
        wait=0.05 * step
        pixels.clear()
        color=(255, 0, 0)
        color1=(0, 255, 0)
        for i in range(1,10):
            pixels.set_pixel(((pixels.count()-1)-1), LED.RGB_to_color( 0, 0, 0 ))
            pixels.set_pixel(step-1, LED.RGB_to_color( 0, 0, 0 ))
            for i in range(0,pixels.count(),step):
                pixels.set_pixel(i, LED.RGB_to_color( color[0], color[1], color[2]  ))
                pixels.set_pixel((pixels.count()-i-1), LED.RGB_to_color( color1[0], color1[1], color1[2] )) 
                if i > 0:
                    pixels.set_pixel(i-step, LED.RGB_to_color( 0, 0, 0 ))
                    pixels.set_pixel((pixels.count()-i -1 + step), LED.RGB_to_color( 0, 0, 0 )) 
                pixels.show()
                
                if wait > 0:
                    time.sleep(wait)

    # blink color Green
    def case_9(self, blink_times=5, wait=0.5, color=(0,255,255)):
        pixels = self.pixels
        for i in range(blink_times):
            if self.should_stop.is_set():
                break
            # blink two times, then wait
            pixels.clear()
            for j in range(2):
                for k in range(pixels.count()):
                    pixels.set_pixel(k, LED.RGB_to_color( color[0], color[1], color[2] ))
                pixels.show()
                time.sleep(0.08)
                pixels.clear()
                pixels.show()
                time.sleep(0.08)
            time.sleep(wait)
    
    # Goal celebration animation - intense rapid blinking for 7 seconds
    def case_10(self):
        pixels = self.pixels
        duration = 7.0  # 7 seconds total
        blink_delay = 0.05  # Very fast blinking
        start_time = time.time()
        
        # Alternate between bright colors
        colors = [
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 255),  # White
        ]
        color_index = 0
        
        while time.time() - start_time < duration:
            if self.should_stop.is_set():
                break
            
            # Fill all pixels with current color
            color = colors[color_index % len(colors)]
            for i in range(pixels.count()):
                pixels.set_pixel(i, LED.RGB_to_color(color[0], color[1], color[2]))
            pixels.show()
            time.sleep(blink_delay)
            
            # Turn off
            pixels.clear()
            pixels.show()
            time.sleep(blink_delay)
            
            # Next color
            color_index += 1                    
