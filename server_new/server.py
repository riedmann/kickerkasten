"""
Flask server for Kickerkasten (foosball table) controller
"""
from flask import Flask, jsonify, request
from timer import Timer
from timer_display import TimerDisplay
from score_manager import ScoreManager
from score_display import ScoreDisplay
from gpio_handler import GPIOHandler
import config

# Initialize Flask app
app = Flask(__name__)

# Initialize displays
print("Initializing displays...")
timer_display = TimerDisplay()
score_display = ScoreDisplay()

# Initialize score manager
score_manager = ScoreManager()

# Define goal callbacks
def on_left_goal():
    """Called when left team scores"""
    score = score_manager.goal_left()
    score_display.update(score['team_left'], score['team_right'])
    print(f"Score updated: {score['team_left']}:{score['team_right']}")

def on_right_goal():
    """Called when right team scores"""
    score = score_manager.goal_right()
    score_display.update(score['team_left'], score['team_right'])
    print(f"Score updated: {score['team_left']}:{score['team_right']}")

# Initialize GPIO handler
print("Initializing GPIO...")
gpio_handler = GPIOHandler(on_left_goal=on_left_goal, on_right_goal=on_right_goal)

# Initialize timer with display
timer = Timer(display=timer_display)
timer.start()  # Start the timer thread
print("Server initialized and running")


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
    return jsonify({
        "action": "start",
        "data": result
    })


@app.route('/timer/stop', methods=['GET'])
def stop_timer():
    """Stop the timer completely"""
    result = timer.stop_timer()
    return jsonify({
        "action": "stop",
        "data": result
    })


@app.route('/timer/pause', methods=['GET'])
def pause_timer():
    """Pause the timer"""
    result = timer.pause_timer()
    return jsonify({
        "action": "pause",
        "data": result
    })


@app.route('/timer/reset', methods=['GET'])
def reset_timer():
    """Reset the timer to default or specified time"""
    time_param = request.args.get('time', type=int)
    result = timer.reset_timer(time_param)
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
    return jsonify(score)


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
    """Homepage with API information"""
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
    print("Starting Kickerkasten Server...")
    print(f"Timer default duration: {config.DEFAULT_TIME_TO_RUN} seconds")
    app.run(debug=False, host='0.0.0.0', port=5000)
