"""
Flask server for Kickerkasten (foosball table) controller
"""
from flask import Flask, jsonify, request, render_template
from .timer import Timer
from .timer_display import TimerDisplay
from .score_manager import ScoreManager
from .score_display import ScoreDisplay
from .gpio_handler import GPIOHandler
from .sound_manager import SoundManager
from .LedHandler import LedHandler
from .mqtt_handler import MQTTHandler
from time import sleep
from . import config

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize displays
timer_display = TimerDisplay()
score_display = ScoreDisplay()

# Initialize score manager
score_manager = ScoreManager()

# Initialize sound manager
sound_manager = SoundManager()

# Initialize LedHandler (will set timer reference later)
led_handler = LedHandler()

# Initialize MQTT handler
mqtt_handler = MQTTHandler(
    broker=config.MQTT_BROKER,
    port=config.MQTT_PORT,
    client_id=config.MQTT_CLIENT_ID
)

# Define goal callbacks
def on_left_goal():
    """Called when left team scores"""
    # Check if timer is running
    if timer.is_running and not timer.is_paused:
        # Valid goal
        sound_manager.play_goal()
        led_handler.runLed(10, loop=False)  # Play goal animation once
        score = score_manager.goal_left()
        score_display.update(score['team_left'], score['team_right'])
    else:
        # Invalid goal - timer not running
        sound_manager.play_nogoal()

def on_right_goal():
    """Called when right team scores"""
    # Check if timer is running
    if timer.is_running and not timer.is_paused:
        # Valid goal
        sound_manager.play_goal()
        led_handler.runLed(10, loop=False)  # Play goal animation once
        score = score_manager.goal_right()
        score_display.update(score['team_left'], score['team_right'])
    else:
        # Invalid goal - timer not running
        sound_manager.play_nogoal()

# Initialize GPIO handler
gpio_handler = GPIOHandler(on_left_goal=on_left_goal, on_right_goal=on_right_goal)

# Define timer end callback
def on_timer_end():
    """Called when timer reaches 0"""
    sound_manager.play_start()
    # Switch to pause animation when game ends
    led_handler.switch_to_pause_mode()

# Initialize timer with display and callback
timer = Timer(display=timer_display, on_timer_end=on_timer_end)
timer.start()  # Start the timer thread

# Set timer reference in LED handler so it can check game state
led_handler.set_timer(timer)

# Set components in MQTT handler and start it
mqtt_handler.set_components(timer, score_manager)
mqtt_handler.start()


@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Timer endpoints
@app.route('/timer/start', methods=['GET'])
def start_timer():
    """Start the countdown timer"""
    result = timer.start_timer()
    sound_manager.play_start()
    # Switch to active game animation (2-9)
    led_handler.switch_to_game_mode()
    return jsonify({
        "action": "start",
        "data": result
    })


@app.route('/timer/stop', methods=['GET'])
def stop_timer():
    """Stop the timer completely"""
    result = timer.stop_timer()
    sound_manager.play_start()
    return jsonify({
        "action": "stop",
        "data": result
    })


@app.route('/timer/pause', methods=['GET'])
def pause_timer():
    """Pause the timer"""
    result = timer.pause_timer()
    sound_manager.play_start()
    # Switch to pause animation (case_1)
    led_handler.switch_to_pause_mode()
    return jsonify({
        "action": "pause",
        "data": result
    })


@app.route('/timer/reset', methods=['GET'])
def reset_timer():
    """Reset the timer to default or specified time"""
    time_param = request.args.get('time', type=int)
    
    # Reset timer first (without display update)
    result = timer.reset_timer_no_display(time_param)
    
    # Reset score
    score = score_manager.reset()
    
    # Update both displays in sequence (they will acquire i2c_lock internally)
    score_display.update(score['team_left'], score['team_right'])
    timer.update_display()

    return jsonify({
        "action": "reset",
        "data": result
    })


@app.route('/timer/status', methods=['GET'])
def get_timer_status():
    """Get current timer status"""
    status = timer.get_status()
    return jsonify(status)


# Score endpoints
@app.route('/score', methods=['GET'])
def get_score():
    """Get current score"""
    score = score_manager.get_score()
    return jsonify({
        "team1": score['team_left'],
        "team2": score['team_right']
    })


@app.route('/score/reset', methods=['GET'])
def reset_score():
    """Reset score to 0:0"""
    score = score_manager.reset()
    score_display.update(score['team_left'], score['team_right'])
    return jsonify({
        "action": "reset",
        "data": score
    })


@app.route('/', methods=['GET'])
def homepage():
    """Serve the main frontend application"""
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api_info():
    """API information and endpoints"""
    return jsonify({
        "name": "Kickerkasten API",
        "version": "2.0",
        "endpoints": {
            "timer": {
                "/timer/start": "Start the timer",
                "/timer/stop": "Stop the timer",
                "/timer/pause": "Pause the timer",
                "/timer/reset": "Reset timer (optional ?time=seconds)",
                "/timer/status": "Get timer status"
            },
            "score": {
                "/score": "Get current score",
                "/score/reset": "Reset score to 0:0"
            },
            "sound": {
                "/sound/on": "Turn background sound on",
                "/sound/off": "Turn background sound off",
                "/sound/plus": "Increase sound volume",
                "/sound/minus": "Decrease sound volume",
                "/sound/normal": "Set sound to normal volume"
            },
            "ball": {
                "/ball/out": "Trigger ball out mechanism"
            },
            "frontend": {
                "/": "Frontend web interface"
            },
            "led": {
                "/led/1": "Trigger LED animation 1",
                "/led/2": "Trigger LED animation 2",
                "/led/3": "Trigger LED animation 3",
                "/led/4": "Trigger LED animation 4",
                "/led/5": "Trigger LED animation 5",
                "/led/6": "Trigger LED animation 6",
                "/led/7": "Trigger LED animation 7",
                "/led/8": "Trigger LED animation 8",
                "/led/9": "Trigger LED animation 9",
                "/led/10": "Trigger LED animation 10"
            }
        }
    })


@app.route('/ball/out', methods=['GET'])
def ball_out():
    """Trigger ball out mechanism (set BALL_OUT pin high for 200ms)"""
    try:
        gpio_handler.ball_output.on()
        from threading import Timer as ThreadingTimer
        ThreadingTimer(0.2, gpio_handler.ball_output.off).start()
        return jsonify({"action": "ball out triggered"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# LED animation endpoints (dynamic)
@app.route('/led/<int:animation_id>', methods=['GET'])
def led_animation(animation_id):
    """Trigger LED animation by ID (1-10)"""
    if 1 <= animation_id <= 10:
        # Animation 10 is for goals (one-time), others loop
        loop = (animation_id != 10)
        led_handler.runLed(animation_id, loop=loop)
        return jsonify({"action": f"LED animation {animation_id} started", "loop": loop})
    else:
        return jsonify({"error": "Animation ID must be between 1 and 10"}), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
