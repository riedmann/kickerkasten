from threading import Thread
from time import sleep
import constant
import sys
import pygame
import gpiohandler

# 7 segement
import board
import busio
from adafruit_ht16k33 import segments

i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

class SevenSegmentTimer(Thread):
    def __init__(self, gpiohandler):
        print("Starting Seven Segment Element...")
        Thread.__init__(self)
        
        # instance variables
        self.timetorun = constant.DEFAULT_TIME_TO_RUN
        self.stop = True
        self.gpio = gpiohandler
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("./sound/start.ogg")
    
        # segment
        self.segment1 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_TIMER_1)
        #self.segment1.begin()
        self.segment2 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_TIMER_2)
        #self.segment2.begin()
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
        self.segment1.fill(0)
        # Set the first character to '1':
        self.segment1[0] = str(int(hour/10))
        # Set the second character to '2':
        self.segment1[1] = str(hour % 10)
        # Set the third character to 'A':
        self.segment1[2] = str(int(minute/10))
        # Set the forth character to 'B':
        self.segment1[3] = str(minute % 10)
        self.segment1.print(':')
        
        self.segment2.fill(0)
        # Set the first character to '1':
        self.segment2[0] = str(int(hour/10))
        # Set the second character to '2':
        self.segment2[1] = str(hour % 10)
        # Set the third character to 'A':
        self.segment2[2] = str(int(minute/10))
        # Set the forth character to 'B':
        self.segment2[3] = str(minute % 10)
        self.segment2.print(':')
        
        
    
   
   
