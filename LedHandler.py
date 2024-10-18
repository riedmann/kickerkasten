from threading import Thread
from LedAnimation import LedAnimation

# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import RPi.GPIO as GPIO
# Import the WS2801 module.
import Adafruit_WS2801 as LED
import Adafruit_GPIO.SPI as SPI

class LedHandler():
    def __init__(self):
        print("Starting Led Animation...")
        # Configure the count of pixels:
        self.PIXEL_COUNT = 160 
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self.pixels = LED.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

    def runLed(self,animationID):
        print("starting animation")
        ledAnimation = LedAnimation(self.pixels)
        th = Thread(target=ledAnimation.printLED,args=(animationID,))
        th.start()
