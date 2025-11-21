"""
Flask server for Kickerkasten (foosball table) controller
"""
from flask import Flask, jsonify, request
from timer import Timer
import config

# Initialize Flask app
app = Flask(__name__)

# Initialize timer
timer = Timer()
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
            }
        }
    })


if __name__ == '__main__':
    print("Starting Kickerkasten Server...")
    print(f"Timer default duration: {config.DEFAULT_TIME_TO_RUN} seconds")
    app.run(debug=False, host='0.0.0.0', port=5000)
