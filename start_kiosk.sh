#!/bin/bash

# Wait for system to be ready
sleep 10

mosquitto_sub -h localhost -t "test" &

# Navigate to the project directory
cd /home/pi/Documents/kickerkasten

# Activate virtual environment
source venv/bin/activate

# Start the Flask server in the background
python3 -m server.server &

# Wait for the server to start
sleep 5

# Start Chromium in kiosk mode
DISPLAY=:0 chromium-browser --kiosk --incognito --disable-infobars --noerrdialogs --disable-session-crashed-bubble http://localhost:3000
