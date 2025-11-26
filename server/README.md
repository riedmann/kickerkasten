# Kickerkasten Server v2.0

A clean Flask-based server for controlling a foosball table with timer functionality.

## Structure

```
server_new/
├── server.py       # Main Flask application
├── timer.py        # Timer class with thread-safe operations
├── config.py       # Configuration settings
└── README.md       # This file
```

## Installation

```bash
cd server_new
pip install flask
```

## Running the Server

```bash
python server.py
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### Timer Control

- **GET /timer/start** - Start the countdown timer
- **GET /timer/stop** - Stop the timer completely
- **GET /timer/pause** - Pause the timer
- **GET /timer/reset** - Reset timer to default time
- **GET /timer/reset?time=180** - Reset timer to specific time (in seconds)
- **GET /timer/status** - Get current timer status

### Example Response

```json
{
  "action": "start",
  "data": {
    "status": "started",
    "time_remaining": 300,
    "is_paused": false
  }
}
```

## Testing

```bash
# Start timer
curl http://localhost:5000/timer/start

# Get status
curl http://localhost:5000/timer/status

# Pause timer
curl http://localhost:5000/timer/pause

# Reset to 3 minutes
curl http://localhost:5000/timer/reset?time=180
```

## Features

- ✅ Thread-safe timer implementation
- ✅ Start, stop, pause, reset functionality
- ✅ Clean separation of concerns
- ✅ CORS enabled for web interfaces
- ✅ RESTful API design
- 🔄 Ready to add: GPIO handlers, display controllers, score tracking
