import RPi.GPIO as GPIO
import os
import time

import constant
from OnOffThread import OnOffThread
import pygame
from SevenSegmentGoals import SevenSegmentGoals

class gpiohandler:

    ################
    # constructor
    ###############
    def __init__(self):
       self.team1 = 0
       self.team2 = 0
       self.balls = 0
       self.isPaused = True
       self.volume = 1.0
       self.sevenSegmentGoals = SevenSegmentGoals()
       
       pygame.mixer.init()
       self.goalsound = pygame.mixer.Sound("/home/pi/Documents/kickerkasten/sound/goal.ogg")
       self.notValidGoal = pygame.mixer.Sound("/home/pi/Documents/kickerkasten/sound/nogoal.ogg")
     
       self.setup_pins()
       self.register_events() 
       

    def setup_pins(self):
       try:
           # Clean up any existing GPIO settings
           GPIO.setwarnings(False)
           GPIO.cleanup()
       except:
           pass
       
       GPIO.setmode(GPIO.BCM)
       
       print("PIN Goal-Left: " + str(constant.GPIO_PIN_LEFT_GOAL))
       print("PIN Goal-Right: " + str(constant.GPIO_PIN_RIGHT_GOAL))
       print("PIN Ball Out:" + str(constant.GPIO_PIN_BALL_OUT))
       print("PIN Ball in Button:" + str(constant.GPIO_PIN_BALL_BUTTON))

       GPIO.setup(constant.GPIO_PIN_LEFT_GOAL, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
       GPIO.setup(constant.GPIO_PIN_RIGHT_GOAL, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
       GPIO.setup(constant.GPIO_PIN_BALL_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
       GPIO.setup(constant.GPIO_PIN_BALL_OUT, GPIO.OUT)
       
    def register_events(self):
       GPIO.add_event_detect(constant.GPIO_PIN_LEFT_GOAL, GPIO.RISING, callback=self.my_callback_goal_1, bouncetime=constant.BOUNCETIME) 
       GPIO.add_event_detect(constant.GPIO_PIN_RIGHT_GOAL, GPIO.RISING, callback=self.my_callback_goal_2, bouncetime=constant.BOUNCETIME) 
       GPIO.add_event_detect(constant.GPIO_PIN_BALL_BUTTON, GPIO.RISING, callback=self.my_callback_give_ball, bouncetime=constant.BOUNCETIME) 

    def my_callback_goal_1(self, channel):
       if self.isPaused:
         print("paused....sorry")
         self.notValidGoal.play()
       else:
         self.goalsound.play()
         self.team1 += 1
         self.showScore()
       

    def my_callback_goal_2(self, channel):
       print("goal2")    
       if self.isPaused:
         print("paused....sorry")
         self.notValidGoal.play()
       else:
         self.team2 += 1
         self.goalsound.play()
         self.showScore()

    def my_callback_give_ball(self,channel):
       self.balls += 1
       self.give_ball()

    def give_ball(self):
       GPIO.output(constant.GPIO_PIN_BALL_OUT, GPIO.HIGH) 
       ofT = OnOffThread(release_relais, 2)
       ofT.start() # used to turn off the relay again

    def reset(self):
       self.team1 = 0
       self.team2 = 0
       self.showScore()

    def showScore(self):
       print("show score on segment")
       self.sevenSegmentGoals.printToSegment(self.team1,self.team2)

def release_relais():
   GPIO.output(constant.GPIO_PIN_BALL_OUT, GPIO.LOW) # aus
