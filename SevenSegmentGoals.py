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
display = segments.Seg7x4(i2c)

class SevenSegmentGoals:
    def __init__(self):
        self.segment1 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment1.begin()
        self.segment2 = segments.Seg7x4(i2c,constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        self.segment2.begin()
        self.printToSegment(0,0)
        

       
    def printToSegment(self, goals1, goals2 ):
        display.fill(0)
        # Set the first character to '1':
        display[0] = '1'
        # Set the second character to '2':
        display[1] = '2'
        # Set the third character to 'A':
        display[2] = 'A'
        # Set the forth character to 'B':
        display[3] = 'B'
        # self.segment1.clear()
        # if goals1 < 10:
        #     #self.segment.set_digit(0, int(goals1 / 10))     # Tens
        #     self.segment1.set_digit(1, goals1 % 10)          # Ones
        # else:
        #     self.segment1.set_digit(0, int(goals1 / 10))     # Tens
        #     self.segment1.set_digit(1, goals1 % 10)          # Ones

        # # Set minutes
        # if goals2 < 10:
        #     #self.segment.set_digit(2, int(goals2 / 10))   # Tens
        #     self.segment1.set_digit(2, goals2 % 10)        # Ones
        # else:
        #     self.segment1.set_digit(2, int(goals2 / 10))   # Tens
        #     self.segment1.set_digit(3, goals2 % 10)   
        # # Toggle colon
        # self.segment1.set_colon(1)              # Toggle colon at 1Hz
        # # Write the display buffer to the har     dware.  This must be called to
        # # update the actual display LEDs.
        # self.segment1.write_display()
    
        # self.segment2.clear()
        # if goals1 < 10:
        #     #self.segment.set_digit(0, int(goals1 / 10))     # Tens
        #     self.segment2.set_digit(1, goals1 % 10)          # Ones
        # else:
        #     self.segment2.set_digit(0, int(goals1 / 10))     # Tens
        #     self.segment2.set_digit(1, goals1 % 10)          # Ones

        # # Set minutes
        # if goals2 < 10:
        #     #self.segment.set_digit(2, int(goals2 / 10))   # Tens
        #     self.segment2.set_digit(2, goals2 % 10)        # Ones
        # else:
        #     self.segment2.set_digit(2, int(goals2 / 10))   # Tens
        #     self.segment2.set_digit(3, goals2 % 10)   
        # # Toggle colon
        # self.segment2.set_colon(1)              # Toggle colon at 1Hz
        # # Write the display buffer to the har     dware.  This must be called to
        # # update the actual display LEDs.
        # self.segment2.write_display()
    
   