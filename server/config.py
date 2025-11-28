# Configuration file for the Kickerkasten server

# GPIO Pins
GPIO_PIN_RIGHT_GOAL = 17
GPIO_PIN_LEFT_GOAL = 27
GPIO_PIN_BALL_BUTTON = 22
GPIO_PIN_BALL_OUT = 23

# I2C Addresses for Seven Segment Displays
SEVEN_SEGMENT_ADDRESS_TIMER_1 = 0x70
SEVEN_SEGMENT_ADDRESS_TIMER_2 = 0x71
SEVEN_SEGMENT_ADDRESS_GOALS_1 = 0x74
SEVEN_SEGMENT_ADDRESS_GOALS_2 = 0x72

# Timer settings
DEFAULT_TIME_TO_RUN = 300  # 5 minutes in seconds
BOUNCETIME = 80  # milliseconds

# MQTT settings
MQTT_ENABLED = True  # Set to False to disable MQTT
MQTT_BROKER = "letto.htlwrn.ac.at"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "kickerkasten"
MQTT_USERNAME = "iot2021"  # Set to your username or None for no authentication
MQTT_PASSWORD = "iot2021"
MQTT_TOPIC_PREFIX = "edu/iot2021"  # Topic prefix for publishing/subscribing

# Paths
SOUND_FOLDER = "/home/pi/Documents/kickerkasten/sound"
