from threading import Thread
import time

# calls a callback after a giveen amount of time
class OnOffThread(Thread):
    
    def __init__(self, callback, duration):
        Thread.__init__(self)
        self.callback = callback
        self.duration = duration
        
    def run(self):
        self.countdown()

    def countdown(self):
        #print("in countdown")
        time.sleep(self.duration)
        #print("sleep over")
        self.callback()

    
   
   