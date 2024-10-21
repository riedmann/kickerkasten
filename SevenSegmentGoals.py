from threading import Thread
from time import sleep
import constant
import sys
import pygame

# 7 segement
import board
import busio
from adafruit_ht16k33 import segments

i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
#display = segments.Seg7x4(i2c)

class SevenSegmentGoals:
    def __init__(self):
        self.segment1 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment2 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        self.printToSegment(0,0)
        

       
    def printToSegment(self, goals1, goals2 ):
        self.segment1.fill(0)
        self.segment2.fill(0)
        # Set the first character to '1':
        if (goals1<10):
            #self.segment1[0] = str(int(goals1 / 10))
            self.segment1[1] = str(goals1)
            self.segment2[1] = str(goals1)
        # Set the second character to '2':
        if (goals1>9):
            self.segment1[0] = str(int(goals1 / 10))
            self.segment1[1] = str(goals1 % 10)
            self.segment2[0] = str(int(goals1 / 10))
            self.segment2[1] = str(goals1 % 10)
        # Set the third character to 'A':
        if (goals2<10):
            self.segment1[2] = str(int(goals1))
            self.segment2[2] = str(int(goals1))
        # Set the forth character to 'B':
        if (goals1>9):
            self.segment1[2] = str(int(goals1 / 10))
            self.segment1[3] = str(goals1 % 10)
            self.segment2[2] = str(int(goals1 / 10))
            self.segment2[3] = str(goals1 % 10)
        self.segment1.print(':')
        self.segment2.print(':')

        self.segment2.fill(0)
       