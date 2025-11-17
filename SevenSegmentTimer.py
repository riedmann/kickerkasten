from threading import Thread
from time import sleep
import constant
import sys
import board
import busio
from adafruit_ht16k33 import segments
import pygame
import gpiohandler

class SevenSegmentTimer(Thread):
    def __init__(self, gpiohandler):
        print("Starting Seven Segment Element...")
        Thread.__init__(self)
        
        # instance variables
        self.timetorun = constant.DEFAULT_TIME_TO_RUN
        self.stop = True
        self.gpio = gpiohandler
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("/home/pi/kickerkasten/sound/start.ogg")
    
        # segment
        i2c = busio.I2C(board.SCL, board.SDA)
        self.segment1 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_TIMER_1)
        self.segment2 = segments.Seg7x4(i2c, address=constant.SEVEN_SEGMENT_ADDRESS_TIMER_2)
        self.printtime()
        

    def set_gpio(self,gpio):
        self.gpio = gpio

    def run(self):
        self.countdown()

    def resettimer(self,timetorun):
        self.timetorun = timetorun
        self.printtime()
        self.stop=True

    def starttimer(self):
        # print("starting")
        self.stop=False

    def stoptimer(self):
        # print("stopping")
        self.stop=True
        self.sound.play()
        self.gpio.isPaused=True
        

    def printtime(self):
        mins, secs = divmod(self.timetorun, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.printToSegment(mins, secs)
    
    def countdown(self):
        while True:
            self.printtime()
            sleep(1)
                        
            if not self.stop and self.timetorun>0:
                self.timetorun -= 1
            else:
                if not self.stop:
                    self.stoptimer()
                
        
    def printToSegment(self, hour, minute):
        # Format the display string
        display_str = "{:02d}{:02d}".format(hour, minute)
        
        # Clear and update segment1
        self.segment1.fill(0)
        self.segment1.print(display_str)
        self.segment1.colon = True
        
        # Clear and update segment2
        self.segment2.fill(0)
        self.segment2.print(display_str)
        self.segment2.colon = True
    
   
   
