from threading import Thread
from time import sleep
import constant
import sys
from Adafruit_LED_Backpack import SevenSegment
import pygame

class SevenSegmentGoals:
    def __init__(self):
        self.segment1 = SevenSegment.SevenSegment(address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_1)
        self.segment1.begin()
        self.segment2 = SevenSegment.SevenSegment(address=constant.SEVEN_SEGMENT_ADDRESS_GOALS_2)
        self.segment2.begin()
        self.printToSegment(0,0)
        

       
    def printToSegment(self, goals1, goals2 ):
        self.segment1.clear()
        if goals1 < 10:
            #self.segment.set_digit(0, int(goals1 / 10))     # Tens
            self.segment1.set_digit(1, goals1 % 10)          # Ones
        else:
            self.segment1.set_digit(0, int(goals1 / 10))     # Tens
            self.segment1.set_digit(1, goals1 % 10)          # Ones

        # Set minutes
        if goals2 < 10:
            #self.segment.set_digit(2, int(goals2 / 10))   # Tens
            self.segment1.set_digit(2, goals2 % 10)        # Ones
        else:
            self.segment1.set_digit(2, int(goals2 / 10))   # Tens
            self.segment1.set_digit(3, goals2 % 10)   
        # Toggle colon
        self.segment1.set_colon(1)              # Toggle colon at 1Hz
        # Write the display buffer to the har     dware.  This must be called to
        # update the actual display LEDs.
        self.segment1.write_display()
    
        self.segment2.clear()
        if goals1 < 10:
            #self.segment.set_digit(0, int(goals1 / 10))     # Tens
            self.segment2.set_digit(1, goals1 % 10)          # Ones
        else:
            self.segment2.set_digit(0, int(goals1 / 10))     # Tens
            self.segment2.set_digit(1, goals1 % 10)          # Ones

        # Set minutes
        if goals2 < 10:
            #self.segment.set_digit(2, int(goals2 / 10))   # Tens
            self.segment2.set_digit(2, goals2 % 10)        # Ones
        else:
            self.segment2.set_digit(2, int(goals2 / 10))   # Tens
            self.segment2.set_digit(3, goals2 % 10)   
        # Toggle colon
        self.segment2.set_colon(1)              # Toggle colon at 1Hz
        # Write the display buffer to the har     dware.  This must be called to
        # update the actual display LEDs.
        self.segment2.write_display()
    
   