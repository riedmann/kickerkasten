from gpiozero import Button, OutputDevice
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
       print("PIN Goal-Left: " + str(constant.GPIO_PIN_LEFT_GOAL))
       print("PIN Goal-Right: " + str(constant.GPIO_PIN_RIGHT_GOAL))
       print("PIN Ball Out:" + str(constant.GPIO_PIN_BALL_OUT))
       print("PIN Ball in Button:" + str(constant.GPIO_PIN_BALL_BUTTON))

       # Setup input buttons with pull-down resistors
       # bounce_time is in seconds (convert ms to seconds)
       bounce_time = constant.BOUNCETIME / 1000.0
       
       self.left_goal_button = Button(constant.GPIO_PIN_LEFT_GOAL, pull_up=False, bounce_time=bounce_time)
       self.right_goal_button = Button(constant.GPIO_PIN_RIGHT_GOAL, pull_up=False, bounce_time=bounce_time)
       self.ball_button = Button(constant.GPIO_PIN_BALL_BUTTON, pull_up=False, bounce_time=bounce_time)
       
       # Setup output for ball release
       self.ball_out = OutputDevice(constant.GPIO_PIN_BALL_OUT, active_high=True, initial_value=False)
       
    def register_events(self):
       self.left_goal_button.when_pressed = self.my_callback_goal_1
       self.right_goal_button.when_pressed = self.my_callback_goal_2
       self.ball_button.when_pressed = self.my_callback_give_ball 

    def my_callback_goal_1(self):
       if self.isPaused:
         print("paused....sorry")
         self.notValidGoal.play()
       else:
         self.goalsound.play()
         self.team1 += 1
         self.showScore()
       

    def my_callback_goal_2(self):
       print("goal2")    
       if self.isPaused:
         print("paused....sorry")
         self.notValidGoal.play()
       else:
         self.team2 += 1
         self.goalsound.play()
         self.showScore()

    def my_callback_give_ball(self):
       self.balls += 1
       self.give_ball()

    def give_ball(self):
       self.ball_out.on()
       ofT = OnOffThread(self.release_relais, 2)
       ofT.start() # used to turn off the relay again
    
    def release_relais(self):
       self.ball_out.off()

    def reset(self):
       self.team1 = 0
       self.team2 = 0
       self.showScore()

    def showScore(self):
       print("show score on segment")
       self.sevenSegmentGoals.printToSegment(self.team1,self.team2)
