# Kickerkasten - Foosball Table Controller

Raspberry Pi-based controller for a foosball table with timer, score tracking, LED animations, and sound effects.

## Features

- **Countdown Timer**: 5-minute game timer with seven-segment displays
- **Automatic Score Tracking**: GPIO-based goal detection for both teams
- **LED Animations**: 160-pixel WS2801 LED strip with 10 different animations
- **Sound Effects**: Audio feedback for goals, game start/end, and invalid goals
- **Ball Dispenser**: Automatic ball release mechanism
- **Web Interface**: REST API and browser-based control panel
- **Kiosk Mode**: Automatic startup for standalone operation

## Hardware Requirements

- Raspberry Pi 5 (or compatible)
- 2x Seven-segment displays (timer) - I2C addresses 0x70, 0x71
- 2x Seven-segment displays (score) - I2C addresses 0x74, 0x72
- WS2801 LED strip (160 pixels)
- GPIO buttons for goal detection (pins 17, 27)
- GPIO ball dispenser control (pins 22, 23)
- Speakers for audio output

## Installation

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# GPIO support for Raspberry Pi 5
pip3 install lgpio

# Adafruit Blinka platform layer
pip3 install adafruit-blinka

# Flask web framework
pip3 install flask

# GPIO Zero library
pip3 install gpiozero

# Seven-segment display driver
pip install adafruit-circuitpython-ht16k33

# Audio playback
pip3 install simpleaudio
```

### 3. Install WS2801 LED Library

```bash
# Clone and install Adafruit WS2801 library
git clone https://github.com/adafruit/Adafruit_Python_WS2801.git
cd Adafruit_Python_WS2801
python3 setup.py install
cd ..
```

## Configuration

Edit `server/config.py` to customize:

- GPIO pin assignments
- I2C addresses for displays
- Default game timer duration (300 seconds)
- Sound file paths

## Running the Server

### Manual Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
python3 -m server.server
```

The server will start on `http://0.0.0.0:5000`

### Automatic Startup (Kiosk Mode)

For automatic startup on boot:

```bash
# Make the startup script executable
chmod +x start_kiosk.sh

# Copy desktop entry to autostart
mkdir -p ~/.config/autostart
cp kickerkasten.desktop ~/.config/autostart/
```

Reboot to test autostart functionality.

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete REST API reference.

### Quick Examples

```bash
# Start the game
curl http://10.72.5.212:5000/timer/start

# Pause the game
curl http://10.72.5.212:5000/timer/pause

# Reset timer and score
curl http://10.72.5.212:5000/timer/reset

# Get current score
curl http://10.72.5.212:5000/score

# Trigger LED animation
curl http://10.72.5.212:5000/led/5
```

## Project Structure

```
kickerkasten/
├── server/
│   ├── server.py              # Flask application
│   ├── timer.py               # Timer logic
│   ├── timer_display.py       # Timer seven-segment displays
│   ├── score_manager.py       # Score tracking
│   ├── score_display.py       # Score seven-segment displays
│   ├── gpio_handler.py        # GPIO button handling
│   ├── sound_manager.py       # Audio playback
│   ├── LedHandler.py          # LED controller
│   ├── LedAnimation.py        # LED animation patterns
│   ├── config.py              # Configuration
│   └── i2c_lock.py            # I2C bus synchronization
├── templates/
│   └── index.html             # Web interface
├── static/                    # CSS, JS, images
├── sound/                     # Audio files
├── start_kiosk.sh            # Kiosk autostart script
├── kickerkasten.desktop      # Desktop autostart entry
├── API_DOCUMENTATION.md      # Complete API reference
└── README.md                 # This file
```

## LED Animations

| ID | Description | Usage |
|----|-------------|-------|
| 1 | Dim moving point | Pause/idle mode |
| 2-9 | Various effects | Active game (random) |
| 10 | Intense celebration | Goal scored (7 seconds) |

**Automatic Behavior:**
- Startup: Animation 1 (paused)
- Game starts: Random animation 2-9
- Game paused: Animation 1
- Goal scored: Animation 10 (once), then returns to previous
- Game ends: Animation 1

## Display System

### Timer Displays
- Format: MM:SS with colon
- Updates every second when running
- Default: 05:00 (300 seconds)

### Score Displays
- Format: X:Y with colon
- Auto-refreshes every 0.5 seconds
- Range: 0-99 per team

## GPIO Configuration

```
GPIO 17: Right team goal button
GPIO 27: Left team goal button
GPIO 22: Ball dispenser button
GPIO 23: Ball dispenser output
```

## Network Configuration

### Set Fixed IP Address

To assign a static IP address to your Raspberry Pi:

#### Method 1: Using dhcpcd (Recommended)

Edit the dhcpcd configuration file:
```bash
sudo nano /etc/dhcpcd.conf
```

Add the following lines at the end (adjust values for your network):
```bash
# Static IP configuration
interface eth0  # Use wlan0 for WiFi
static ip_address=10.72.5.212/24
static routers=10.72.5.1
static domain_name_servers=10.72.5.1 8.8.8.8
```

Save and reboot:
```bash
sudo reboot
```

#### Method 2: Using NetworkManager (Raspberry Pi OS Bookworm)

```bash
# For Ethernet
sudo nmcli con mod "Wired connection 1" ipv4.addresses 10.72.5.212/24
sudo nmcli con mod "Wired connection 1" ipv4.gateway 10.72.5.1
sudo nmcli con mod "Wired connection 1" ipv4.dns "10.72.5.1 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"

# For WiFi (replace "YourWiFiName" with your SSID)
sudo nmcli con mod "YourWiFiName" ipv4.addresses 10.72.5.212/24
sudo nmcli con mod "YourWiFiName" ipv4.gateway 10.72.5.1
sudo nmcli con mod "YourWiFiName" ipv4.dns "10.72.5.1 8.8.8.8"
sudo nmcli con mod "YourWiFiName" ipv4.method manual
sudo nmcli con up "YourWiFiName"
```

#### Verify Configuration

```bash
# Check IP address
ip addr show

# Check connectivity
ping -c 4 8.8.8.8
```

**Network Settings Explanation:**
- `ip_address`: Your desired static IP with subnet mask (e.g., 10.72.5.212/24)
- `routers`: Your router/gateway IP address
- `domain_name_servers`: DNS servers (your router and/or Google DNS 8.8.8.8)

## Troubleshooting

### I2C Devices Not Found
```bash
# Enable I2C interface
sudo raspi-config
# Navigate to Interface Options -> I2C -> Enable

# Check connected devices
i2cdetect -y 1
```

### Permission Denied on GPIO
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
# Log out and back in
```

### LED Strip Not Working
```bash
# Check SPI is enabled
ls /dev/spidev*
# Should show: /dev/spidev0.0 /dev/spidev0.1

# Enable SPI if needed
sudo raspi-config
# Navigate to Interface Options -> SPI -> Enable
```

### Audio Not Playing
```bash
# Check audio output
aplay -l

# Test audio file
aplay sound/start.wav
```

## Development

### Running in Development Mode

Edit `server/server.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Testing LED Animations

Use the standalone test script:
```bash
python3 ws2801_test.py
```

## License

See LICENSE.txt for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

## Authors

- Andreas Riedmann

## Acknowledgments

- Adafruit for hardware libraries
- Flask for web framework
- gpiozero for GPIO abstraction
