import time
import RPi.GPIO as GPIO
import Adafruit_WS2801 as LED
import Adafruit_GPIO.SPI as SPI

PIXEL_COUNT = 160  # Change to your number of LEDs
SPI_PORT = 0
SPI_DEVICE = 0

pixels = LED.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def all_on(color):
    for i in range(PIXEL_COUNT):
        pixels.set_pixel_rgb(i, *color)
    pixels.show()

def all_off():
    for i in range(PIXEL_COUNT):
        pixels.set_pixel_rgb(i, 0, 0, 0)
    pixels.show()

def color_chase():
    for i in range(PIXEL_COUNT):
        pixels.set_pixel_rgb(i, 255, 0, 0)  # Red
        pixels.show()
        time.sleep(0.01)
    for i in range(PIXEL_COUNT):
        pixels.set_pixel_rgb(i, 0, 255, 0)  # Green
        pixels.show()
        time.sleep(0.01)
    for i in range(PIXEL_COUNT):
        pixels.set_pixel_rgb(i, 0, 0, 255)  # Blue
        pixels.show()
        time.sleep(0.01)
    all_off()

if __name__ == "__main__":
    try:
        print("All LEDs red for 2 seconds...")
        all_on((255, 0, 0))
        time.sleep(2)
        print("All LEDs green for 2 seconds...")
        all_on((0, 255, 0))
        time.sleep(2)
        print("All LEDs blue for 2 seconds...")
        all_on((0, 0, 255))
        time.sleep(2)
        print("Color chase...")
        color_chase()
        print("All off.")
        all_off()
    except KeyboardInterrupt:
        all_off()
        print("Test interrupted, all LEDs off.")
