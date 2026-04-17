#!/bin/bash

# Wait for system to be ready
sleep 10

# Navigate to the project directory
cd /home/pi/Documents/kickerkasten

# Kill any existing Python server processes to release GPIO
echo "Checking for existing Python processes..."
pkill -9 -f "python3 -m server.server" 2>/dev/null && echo "Killed existing server process" || echo "No existing server process found"
sleep 2

# Activate virtual environment
source venv/bin/activate

# Start the Flask server in the background
python3 -m server.server 

# Wait for the server to start
sleep 5

# Start Chromium in kiosk mode
DISPLAY=:0 chromium-browser --kiosk --incognito --disable-infobars --noerrdialogs --disable-session-crashed-bubble http://localhost:3000
