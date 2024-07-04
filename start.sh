#!/bin/bash
# Mauszeiger ausblenden
#/usr/bin/unclutter &
# Bildschirmschoner ausschalten
#xscreensaver -no-splash  
#xset s off
#xset -dpms
#xset s noblank
# Chromium starten und euredomain.de aufrufen
#cd /home/raspi/coding

echo Switching

source /home/raspi/coding/.venv/bin/activate
which python
python3 /home/raspi/coding/kickerkasten/server.py &
DISPLAY=:0 chromium-browser http://127.0.0.1:5000 --start-fullscreen --kiosk --incognito --noerrdialogs --no-first-run --disk-cache-dir=/dev/null  &
#chromium-browser https://www.orf.at
$SHELL
