#!/bin/bash
# Script to cleanup GPIO and kill all server processes

echo "=== GPIO Cleanup Script ==="

# Kill all Python processes
echo "Killing all Python processes..."
sudo pkill -9 python3
sudo pkill -9 python
sleep 1

# Check if any are still running
if pgrep -f "python" > /dev/null; then
    echo "Warning: Some Python processes are still running"
    ps aux | grep python | grep -v grep
else
    echo "✓ All Python processes terminated"
fi

# Check what's using GPIO
echo ""
echo "Checking GPIO memory access..."
lsof /dev/gpiomem 2>/dev/null | grep -v "COMMAND" && echo "Warning: GPIO still in use" || echo "✓ GPIO is free"

# Check what's using gpiochip
lsof /dev/gpiochip* 2>/dev/null | grep -v "COMMAND" && echo "Warning: GPIO chip still in use" || echo "✓ GPIO chip is free"

echo ""
echo "=== Cleanup complete ==="
echo "You can now start the server with: ./start_kiosk.sh"
