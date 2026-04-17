#!/bin/bash

echo "=== Kickerkasten Kiosk Startup ==="
echo "Waiting for system to be ready..."
sleep 10

# Navigate to the project directory
echo "Navigating to project directory..."
cd /home/pi/Documents/kickerkasten

# Kill any existing Python server processes to release GPIO
echo "Checking for existing Python processes..."
pkill -9 -f "python3 -m server.server" 2>/dev/null && echo "✓ Killed existing server process" || echo "✓ No existing server process found"
sleep 2

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start the Flask server in the background
echo "Starting Flask server..."
python3 -m server.server &
SERVER_PID=$!
echo "✓ Server started with PID: $SERVER_PID"

# Wait for the server to start
echo "Waiting for server to initialize..."
sleep 5

# Check if server is still running
if ps -p $SERVER_PID > /dev/null; then
    echo "✓ Server is running"
else
    echo "✗ ERROR: Server failed to start!"
    exit 1
fi

# Start Chromium in kiosk mode
#echo "Starting Chromium in kiosk mode..."
#DISPLAY=:0 chromium-browser --kiosk --incognito --disable-infobars --noerrdialogs --disable-session-crashed-bubble http://localhost:3000
