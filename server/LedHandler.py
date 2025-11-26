from threading import Thread
from LedAnimation import LedAnimation
import RPi.GPIO as GPIO
import Adafruit_WS2801 as LED
import Adafruit_GPIO.SPI as SPI

class LedHandler:
    def __init__(self, pixel_count=160, spi_port=0, spi_device=0):
        print("Starting LedHandler...")
        self.PIXEL_COUNT = pixel_count
        self.pixels = LED.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(spi_port, spi_device), gpio=GPIO)

    def runLed(self, animationID):
        print(f"Starting animation {animationID}")
        ledAnimation = LedAnimation(self.pixels)
        th = Thread(target=ledAnimation.printLED, args=(animationID,))
        th.start()
