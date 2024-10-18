import time
import adafruit_ws2801 as LED

class LedAnimation:
    def __init__(self, pixels):
        self.pixels = pixels
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!

    def printLED(self, animationId):
        # Dynamically call the appropriate case method based on animationId
        getattr(self, 'case_' + str(animationId), lambda: 'nothing')()
        self.pixels.clear()
        self.pixels.show()

    # Custom RGB to color conversion function
    def RGB_to_color(self, red, green, blue):
        return (red << 16) | (green << 8) | blue

    # Define the wheel function to interpolate between different hues
    def wheel(self, pos):
        if pos < 85:
            return self.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return self.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return self.RGB_to_color(0, pos * 3, 255 - pos * 3)

    # rainbow_cycle_successive
    def case_1(self):
        pixels = self.pixels
        wait = 0.1
        for i in range(pixels.count()):
            pixels.set_pixel(i, self.wheel((i * 256 // pixels.count()) % 256))
            pixels.show()
            if wait > 0:
                time.sleep(wait)

    # appear from back
    def case_2(self):
        pixels = self.pixels
        color = (255, 0, 0)
        for i in range(pixels.count()):
            for j in reversed(range(i, pixels.count())):
                pixels.clear()
                for k in range(i):
                    pixels.set_pixel(k, self.RGB_to_color(color[0], color[1], color[2]))
                pixels.set_pixel(j, self.RGB_to_color(color[0], color[1], color[2]))
                pixels.show()
                time.sleep(0.03)

    # rainbow_cycle
    def case_3(self):
        pixels = self.pixels
        wait = 0.005
        for j in range(256):
            for i in range(pixels.count()):
                pixels.set_pixel(i, self.wheel(((i * 256 // pixels.count()) + j) % 256))
            pixels.show()
            if wait > 0:
                time.sleep(wait)

    # rainbow_colors
    def case_4(self):
        pixels = self.pixels
        wait = 0.01
        for j in range(256):
            for i in range(pixels.count()):
                pixels.set_pixel(i, self.wheel((256 // pixels.count() + j) % 256))
            pixels.show()
            if wait > 0:
                time.sleep(wait)

    # brightness_decrease
    def case_5(self):
        pixels = self.pixels
        wait = 0.01
        step = 1
        for j in range(int(256 // step)):
            for i in range(pixels.count()):
                r, g, b = pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                pixels.set_pixel(i, self.RGB_to_color(r, g, b))
            pixels.show()
            if wait > 0:
                time.sleep(wait)

    # blink color Red
    def case_6(self, blink_times=5, wait=0.5, color=(255, 0, 0)):
        pixels = self.pixels
        for i in range(blink_times):
            pixels.clear()
            for j in range(2):
                for k in range(pixels.count()):
                    pixels.set_pixel(k, self.RGB_to_color(color[0], color[1], color[2]))
                pixels.show()
                time.sleep(0.08)
                pixels.clear()
                pixels.show()
                time.sleep(0.08)
            time.sleep(wait)

    # Multiple color blink sequence
    def case_7(self):
        for _ in range(1):
            self.case_6(blink_times=1, color=(255, 0, 0))
            self.case_6(blink_times=1, color=(0, 255, 0))
            self.case_6(blink_times=1, color=(0, 0, 255))

    # Alternating color pattern
    def case_8(self):
        pixels = self.pixels
        step = 2
        wait = 0.05 * step
        pixels.clear()
        color = (255, 0, 0)
        color1 = (0, 255, 0)
        for _ in range(1, 10):
            pixels.set_pixel(pixels.count() - 1, self.RGB_to_color(0, 0, 0))
            for i in range(0, pixels.count(), step):
                pixels.set_pixel(i, self.RGB_to_color(color[0], color[1], color[2]))
                pixels.set_pixel(pixels.count() - i - 1, self.RGB_to_color(color1[0], color1[1], color1[2]))
                if i > 0:
                    pixels.set_pixel(i - step, self.RGB_to_color(0, 0, 0))
                    pixels.set_pixel(pixels.count() - i - 1 + step, self.RGB_to_color(0, 0, 0))
                pixels.show()
                if wait > 0:
                    time.sleep(wait)

    # blink color Green
    def case_9(self, blink_times=5, wait=0.5, color=(0, 255, 255)):
        pixels = self.pixels
        for _ in range(blink_times):
            pixels.clear()
            for _ in range(2):
                for k in range(pixels.count()):
                    pixels.set_pixel(k, self.RGB_to_color(color[0], color[1], color[2]))
                pixels.show()
                time.sleep(0.08)
                pixels.clear()
                pixels.show()
                time.sleep(0.08)
            time.sleep(wait)
