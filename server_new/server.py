"""
Flask server for Kickerkasten (foosball table) controller
"""
from flask import Flask, jsonify, request, render_template
from timer import Timer
from timer_display import TimerDisplay
from score_manager import ScoreManager
from score_display import ScoreDisplay
from gpio_handler import GPIOHandler
from sound_manager import SoundManager
from time import sleep
import config

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize displays
timer_display = TimerDisplay()
score_display = ScoreDisplay()

# Initialize score manager
score_manager = ScoreManager()

# Initialize sound manager
sound_manager = SoundManager()

# Define goal callbacks
def on_left_goal():
    """Called when left team scores"""
    # Check if timer is running
    if timer.is_running and not timer.is_paused:
        # Valid goal
        sound_manager.play_goal()
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
        score = score_manager.goal_right()
        score_display.update(score['team_left'], score['team_right'])
    else:
        # Invalid goal - timer not running
        sound_manager.play_nogoal()

# Initialize GPIO handler
gpio_handler = GPIOHandler(on_left_goal=on_left_goal, on_right_goal=on_right_goal)

# Initialize timer with display
timer = Timer(display=timer_display)
timer.start()  # Start the timer thread


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
    return jsonify({
        "action": "pause",
        "data": result
    })


@app.route('/timer/reset', methods=['GET'])
def reset_timer():
    """Reset the timer to default or specified time"""
    time_param = request.args.get('time', type=int)
    result = timer.reset_timer(time_param)
    
    # Reset score to 0:0
    score = score_manager.reset()
    sleep(0.1)  # Brief delay to avoid I2C conflicts
    score_display.update(score['team_left'], score['team_right'])
    
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
            }
        }
    })


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
