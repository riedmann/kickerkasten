# Kickerkasten API Documentation

**Base URL:** `http://10.72.5.212:5000`  
**Version:** 2.0

## Overview

REST API for controlling a foosball table (Kickerkasten) with timer, score tracking, LED animations, sound effects, and ball dispenser.

---

## Timer Endpoints

### Start Timer
**Endpoint:** `GET /timer/start`

Starts or resumes the countdown timer and switches LED to active game mode (random animation 2-9).

**Response:**
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

**Side Effects:**
- Plays start sound
- Switches LED to random animation (2-9)

---

### Stop Timer
**Endpoint:** `GET /timer/stop`

Stops the timer completely.

**Response:**
```json
{
  "action": "stop",
  "data": {
    "status": "stopped",
    "time_remaining": 245,
    "is_paused": true
  }
}
```

**Side Effects:**
- Plays start sound

---

### Pause Timer
**Endpoint:** `GET /timer/pause`

Pauses the timer without resetting.

**Response:**
```json
{
  "action": "pause",
  "data": {
    "status": "paused",
    "time_remaining": 180,
    "is_paused": true
  }
}
```

**Side Effects:**
- Plays start sound
- Switches LED to pause mode (animation 1)

---

### Reset Timer
**Endpoint:** `GET /timer/reset`

Resets timer to default (300 seconds) or specified time, and resets score to 0:0.

**Query Parameters:**
- `time` (optional, integer): Time in seconds to reset to (default: 300)

**Request Examples:**
```
GET /timer/reset
GET /timer/reset?time=420
```

**Response:**
```json
{
  "action": "reset",
  "data": {
    "status": "reset",
    "time_remaining": 300,
    "is_paused": true
  }
}
```

**Side Effects:**
- Resets score to 0:0
- Updates timer display to 05:00
- Updates score display to 0:0

---

### Get Timer Status
**Endpoint:** `GET /timer/status`

Retrieves current timer status.

**Response:**
```json
{
  "time_remaining": 245,
  "time_formatted": "04:05",
  "is_running": true,
  "is_paused": false
}
```

**Fields:**
- `time_remaining`: Seconds remaining
- `time_formatted`: MM:SS format
- `is_running`: Timer is active
- `is_paused`: Timer is paused

---

## Score Endpoints

### Get Score
**Endpoint:** `GET /score`

Retrieves current score.

**Response:**
```json
{
  "team1": 3,
  "team2": 5
}
```

**Fields:**
- `team1`: Left team score
- `team2`: Right team score

---

### Reset Score
**Endpoint:** `GET /score/reset`

Resets score to 0:0 without affecting timer.

**Response:**
```json
{
  "action": "reset",
  "data": {
    "team_left": 0,
    "team_right": 0
  }
}
```

**Side Effects:**
- Updates score display to 0:0

---

## LED Animation Endpoints

### Trigger LED Animation
**Endpoint:** `GET /led/<animation_id>`

Triggers LED animation by ID (1-10).

**Path Parameters:**
- `animation_id` (integer, 1-10): Animation number

**Request Examples:**
```
GET /led/1
GET /led/5
GET /led/10
```

**Response (Success):**
```json
{
  "action": "LED animation 5 started",
  "loop": true
}
```

**Response (Error):**
```json
{
  "error": "Animation ID must be between 1 and 10"
}
```
**HTTP Status:** 400

**Animation Behaviors:**
- **Animation 1**: Simple dim moving point (pause mode)
- **Animations 2-9**: Various effects, loop continuously
- **Animation 10**: Intense 7-second goal celebration (plays once)

**Automatic Triggers:**
- Animation 1: Shown when game is paused or ended
- Animations 2-9: Random selection when game starts
- Animation 10: Triggered automatically on valid goals

---

## Ball Dispenser Endpoint

### Trigger Ball Output
**Endpoint:** `GET /ball/out`

Activates ball dispenser mechanism (200ms pulse on GPIO pin 23).

**Response (Success):**
```json
{
  "action": "ball out triggered"
}
```

**Response (Error):**
```json
{
  "error": "error message"
}
```
**HTTP Status:** 500

---

## Frontend Endpoint

### Homepage
**Endpoint:** `GET /`

Serves the main web interface.

**Response:** HTML page (index.html)

---

## API Information Endpoint

### Get API Info
**Endpoint:** `GET /api`

Returns API metadata and endpoint list.

**Response:**
```json
{
  "name": "Kickerkasten API",
  "version": "2.0",
  "endpoints": {
    "timer": {
      "/timer/start": "Start the timer",
      "/timer/stop": "Stop the timer",
      "/timer/pause": "Pause the timer",
      "/timer/reset": "Reset timer (optional ?time=seconds)",
      "/timer/status": "Get timer status"
    },
    "score": {
      "/score": "Get current score",
      "/score/reset": "Reset score to 0:0"
    },
    "sound": {
      "/sound/on": "Turn background sound on",
      "/sound/off": "Turn background sound off",
      "/sound/plus": "Increase sound volume",
      "/sound/minus": "Decrease sound volume",
      "/sound/normal": "Set sound to normal volume"
    },
    "ball": {
      "/ball/out": "Trigger ball out mechanism"
    },
    "frontend": {
      "/": "Frontend web interface"
    },
    "led": {
      "/led/1": "Trigger LED animation 1",
      "/led/2": "Trigger LED animation 2",
      "/led/3": "Trigger LED animation 3",
      "/led/4": "Trigger LED animation 4",
      "/led/5": "Trigger LED animation 5",
      "/led/6": "Trigger LED animation 6",
      "/led/7": "Trigger LED animation 7",
      "/led/8": "Trigger LED animation 8",
      "/led/9": "Trigger LED animation 9",
      "/led/10": "Trigger LED animation 10"
    }
  }
}
```

---

## CORS Headers

All responses include CORS headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type,Authorization
Access-Control-Allow-Methods: GET,PUT,POST,DELETE
```

---

## GPIO Integration

### Goal Detection
Goals are automatically detected via GPIO buttons:
- **Left Goal:** GPIO pin 27
- **Right Goal:** GPIO pin 17

**Behavior on Valid Goal (Timer Running):**
1. Plays goal sound effect
2. Triggers LED animation 10 (7-second celebration)
3. Increments team score
4. Updates score display
5. Returns to previous LED animation

**Behavior on Invalid Goal (Timer Paused):**
1. Plays "no goal" sound effect
2. No score change

---

## Timer Behavior

### Default Settings
- **Default Time:** 300 seconds (5 minutes)
- **Initial State:** Paused

### When Timer Reaches 0:
1. Timer stops automatically
2. Plays start sound
3. Switches LED to pause mode (animation 1)
4. Goals no longer count

---

## LED Animation Details

| ID | Name | Description | Mode | Duration |
|----|------|-------------|------|----------|
| 1 | Pause | Dim moving point | Loop | Continuous |
| 2 | Appear from back | Red pixels appearing | Loop | Continuous |
| 3 | Rainbow cycle | Rainbow wheel effect | Loop | Continuous |
| 4 | Rainbow colors | Solid color rotation | Loop | Continuous |
| 5 | Brightness decrease | Fade out effect | Loop | Continuous |
| 6 | Blink red | Red blinking pattern | Loop | Continuous |
| 7 | RGB blink | Red/Green/Blue cycle | Loop | Continuous |
| 8 | Dual chase | Red/Green chase effect | Loop | Continuous |
| 9 | Blink cyan | Cyan blinking pattern | Loop | Continuous |
| 10 | Goal celebration | Intense rapid color flash | Once | 7 seconds |

**LED Strip:** 160 WS2801 pixels on SPI (port 0, device 0)

---

## Display System

### Timer Displays
- **I2C Addresses:** 0x70, 0x71
- **Format:** MM:SS with colon
- **Auto-update:** Every second when running

### Score Displays
- **I2C Addresses:** 0x74, 0x72
- **Format:** X:Y with colon (e.g., "3:5")
- **Auto-refresh:** Every 0.5 seconds
- **Range:** 0-99 per team

---

## Error Handling

All endpoints use proper HTTP status codes:
- **200 OK:** Successful operation
- **400 Bad Request:** Invalid parameters
- **500 Internal Server Error:** Server-side errors

Error responses include descriptive messages:
```json
{
  "error": "Description of what went wrong"
}
```

---

## Notes

1. **Thread Safety:** All I2C operations use locking with 2-second timeout
2. **Sound Files:** Located in `/home/pi/Documents/kickerkasten/sound/`
3. **GPIO Library:** gpiozero with LGPIOFactory (Raspberry Pi 5)
4. **Server:** Flask on `0.0.0.0:5000`
