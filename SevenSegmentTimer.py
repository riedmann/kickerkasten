from threading import Thread
from time import sleep
import constant
import sys
from Adafruit_LED_Backpack import SevenSegment
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
        self.segment1 = SevenSegment.SevenSegment(address=constant.SEVEN_SEGMENT_ADDRESS_TIMER_1)
        self.segment1.begin()
        self.segment2 = SevenSegment.SevenSegment(address=constant.SEVEN_SEGMENT_ADDRESS_TIMER_2)
        self.segment2.begin()
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
                
        
    def printToSegment(self, hour, minute ):
        self.segment1.clear()
        self.segment1.set_digit(0, int(hour / 10))     # Tens
        self.segment1.set_digit(1, hour % 10)          # Ones
        # Set minutes
        self.segment1.set_digit(2, int(minute / 10))   # Tens
        self.segment1.set_digit(3, minute % 10)        # Ones
        # Toggle colon
        self.segment1.set_colon(1)              # Toggle colon at 1Hz
        # Write the display buffer to the har     dware.  This must be called to
        # update the actual display LEDs.
        self.segment1.write_display()
        self.segment2.clear()
        self.segment2.set_digit(0, int(hour / 10))     # Tens
        self.segment2.set_digit(1, hour % 10)          # Ones
        # Set minutes
        self.segment2.set_digit(2, int(minute / 10))   # Tens
        self.segment2.set_digit(3, minute % 10)        # Ones
        # Toggle colon
        self.segment2.set_colon(1)              # Toggle colon at 1Hz
        # Write the display buffer to the har     dware.  This must be called to
        # update the actual display LEDs.
        self.segment2.write_display()
    
   
   
