#!/bin/bash
# Installation script for Kickerkasten autostart service

echo "Installing Kickerkasten service..."

# Copy the service file to systemd directory
sudo cp /home/pi/Documents/kickerkasten/kickerkasten.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable kickerkasten.service

echo "Service installed successfully!"
echo ""
echo "Useful commands:"
echo "  Start service:   sudo systemctl start kickerkasten"
echo "  Stop service:    sudo systemctl stop kickerkasten"
echo "  Check status:    sudo systemctl status kickerkasten"
echo "  View logs:       sudo journalctl -u kickerkasten -f"
echo "  Disable autostart: sudo systemctl disable kickerkasten"
echo "|"
echo "The service will now start automatically on boot."
echo "To start it now, run: sudo systemctl start kickerkasten"
