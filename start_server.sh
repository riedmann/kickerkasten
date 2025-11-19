  GNU nano 7.2                                                                                             start_server_and_browser.sh                                                                                                      
#!/bin/bash
# Activate virtual environment if needed
source /home/pi/Documents/kickerkasten/venv/bin/activate

# Start the Flask server in background
python3 /home/pi/Documents/kickerkasten/server.py &
SERVER_PID=$!

# Give the server a few seconds to start
sleep 5

# Set DISPLAY variable if not already set
export DISPLAY=${DISPLAY:-:0}

# Check if X server is running before launching browser
if xset q &>/dev/null; then
    # Open Chromium in kiosk mode (fullscreen) pointing to localhost:5000
    # Flags to suppress GPU errors and improve performance on Raspberry Pi
    chromium-browser --kiosk \
        --disable-gpu \
        --disable-software-rasterizer \
        --disable-dev-shm-usage \
        --no-sandbox \
        --disable-features=VizDisplayCompositor \
        http://localhost:5000 &
    BROWSER_PID=$!
else
    echo "No X server detected. Server is running at http://localhost:5000"
    echo "Access the interface from a browser or run this script from the desktop environment."
fi

# Keep script running and wait for the server process
wait $SERVER_PID
