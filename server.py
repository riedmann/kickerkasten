from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import make_response
from gpiohandler import gpiohandler
from SevenSegmentTimer import SevenSegmentTimer
from flask import render_template
#xfrom LedHandler import LedHandler
import constant
import pygame

#LedHandler = LedHandler()
GPIOHandler = gpiohandler()
pygame.mixer.init()
backgroundSound = pygame.mixer.Sound("/home/pi/Documents/kickerkasten/sound/background.ogg")
startSound = pygame.mixer.Sound("/home/pi/Documents/kickerkasten/sound/start.ogg")

global timer;
timer = SevenSegmentTimer(GPIOHandler)
timer.set_gpio(GPIOHandler)
app = Flask(__name__)
soundStep = 0.2;

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/', methods=['GET'])
def homepage():
  return render_template("index.html")

@app.route('/timer/start', methods=['GET'])
def start_timer():
  global timer;
  timer.starttimer()  
  GPIOHandler.isPaused=False
  startSound.play()
  response = jsonify({"action":"staret"})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/timer/pause', methods=['GET'])
def stop_timer():
  timer.stoptimer()  
  
  startSound.play()
  response = jsonify({"action":"stop"})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/timer/reset', methods=['GET'])
def reset_timer():
  time = request.args.get('time')
  GPIOHandler.isPaused=True
  if time is None:
    timer.resettimer(constant.DEFAULT_TIME_TO_RUN)
  else:
    timer.resettimer(int(time))
  
  GPIOHandler.reset()
  response = jsonify({"action":"reset "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/score', methods=['GET'])
def get_score():
  response =jsonify({"team1": GPIOHandler.team1, "team2":GPIOHandler.team2})
  return response

@app.route('/ball/out', methods=['GET'])
def give_ball():
  GPIOHandler.give_ball()
  response = jsonify({"action":"ball out "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/led/<code>')
def led_code(code):
    if code.isnumeric():
        #ledHandler.runLed(int(code));
        return make_response(jsonify({"info":"OK",}),200)
    else:
        return make_response(jsonify({"info":"Led Error Code " + code,}),301)


@app.route('/sound/on', methods=['GET'])
def sound_on():
  backgroundSound.play(-1)
  response = jsonify({"action":"sound on "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response 

@app.route('/sound/off', methods=['GET'])
def sound_off():
  backgroundSound.stop()
  response = jsonify({"action":"sound off "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/sound/plus', methods=['GET'])
def sound_plus():
  set_sound(soundStep)
  response = jsonify({"action":"sound plus volume:"+str(GPIOHandler.volume)})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response
  
@app.route('/sound/minus', methods=['GET'])
def sound_minus():
  set_sound(-soundStep)
  response = jsonify({"action":"sound minus volume:"+str(GPIOHandler.volume)})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/sound/normal', methods=['GET'])
def sound_normal():
  set_sound(2)
  response = jsonify({"action":"sound normal (1) "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


def set_sound(volume):
  GPIOHandler.volume = GPIOHandler.volume + volume  
  if GPIOHandler.volume > 1:
    GPIOHandler.volume = 1
  if GPIOHandler.volume < 0.11:
    GPIOHandler.volume = 0
  pygame.mixer.music.set_volume(GPIOHandler.volume)
  backgroundSound.set_volume(GPIOHandler.volume)

if __name__ == '__main__':
    timer.start()  # Start the timer before running the app
    app.run(debug=False, host= '0.0.0.0', port=5000)
   
