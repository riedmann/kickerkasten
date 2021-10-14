from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import make_response
from gpiohandler import gpiohandler
from SevenSegmentTimer import SevenSegmentTimer
from flask import render_template
from LedHandler import LedHandler
import constant
import pygame

ledHandler = LedHandler()
gpio = gpiohandler()
pygame.mixer.init()
bgsound = pygame.mixer.Sound("/home/pi/kickerkasten/sound/background.ogg")
start = pygame.mixer.Sound("/home/pi/kickerkasten/sound/start.ogg")

global timer;
timer = SevenSegmentTimer(gpio)
timer.set_gpio(gpio)
app = Flask(__name__)
soundStep = 0.2;

@app.before_first_request
def activate_job(): 
    timer.start()

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
  gpio.isPaused=False
  start.play()
  response = jsonify({"action":"staret"})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/timer/pause', methods=['GET'])
def stop_timer():
  timer.stoptimer()  
  gpio.isPaused=True
  start.play()
  response = jsonify({"action":"stop"})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/timer/reset', methods=['GET'])
def reset_timer():
  time = request.args.get('time')
  gpio.isPaused=True
  if time is None:
    timer.resettimer(constant.DEFAULT_TIME_TO_RUN)
  else:
    timer.resettimer(int(time))
  
  gpio.reset()
  response = jsonify({"action":"reset "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/score', methods=['GET'])
def get_score():
  response =jsonify({"team1": gpio.team1, "team2":gpio.team2})
  return response

@app.route('/ball/out', methods=['GET'])
def give_ball():
  gpio.give_ball()
  response = jsonify({"action":"ball out "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/led/<code>')
def led_code(code):
    if code.isnumeric():
        ledHandler.runLed(int(code));
        return make_response(jsonify({"info":"OK",}),200)
    else:
        return make_response(jsonify({"info":"Led Error Code " + code,}),301)


@app.route('/sound/on', methods=['GET'])
def sound_on():
  bgsound.play(-1)
  response = jsonify({"action":"sound on "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response 

@app.route('/sound/off', methods=['GET'])
def sound_off():
  bgsound.stop()
  response = jsonify({"action":"sound off "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/sound/plus', methods=['GET'])
def sound_plus():
  set_sound(soundStep)
  response = jsonify({"action":"sound plus volume:"+str(gpio.volume)})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response
  
@app.route('/sound/minus', methods=['GET'])
def sound_minus():
  set_sound(-soundStep)
  response = jsonify({"action":"sound minus volume:"+str(gpio.volume)})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

@app.route('/sound/normal', methods=['GET'])
def sound_normal():
  set_sound(2)
  response = jsonify({"action":"sound normal (1) "})
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


def set_sound(volume):
  gpio.volume = gpio.volume + volume  
  if gpio.volume > 1:
    gpio.volume = 1
  if gpio.volume < 0.11:
    gpio.volume = 0
  pygame.mixer.music.set_volume(gpio.volume)
  bgsound.set_volume(gpio.volume)

if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0', port=5000)
   
