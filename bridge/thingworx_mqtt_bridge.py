import requests
import time
import paho.mqtt.client as mqtt
from requests.auth import HTTPBasicAuth

# === KONFIGURATION ===

# ThingWorx
THINGWORX_URL = "https://seminar-wer-dornbirn.cloud.arge3d.at/Thingworx"
THING_NAME = "Kicker"
TW_USER = "Administrator"
TW_PASSWORD = "JffzAU5913rRiF"

# MQTT
MQTT_BROKER = "mqtt://letto.htlwrn.ac.at"
MQTT_PORT = 1883
MQTT_USER = "iot2021"
MQTT_PASSWORD = "iot2021"
MQTT_TOPIC = "edu/IOT2021"

# =====================

# MQTT Client einrichten
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("ThingWorx → MQTT Bridge gestartet...")

while True:
    try:
        # Property von ThingWorx abrufen
        r = requests.get(
            f"{THINGWORX_URL}/Things/{THING_NAME}/Properties/OutboundCommand",
            auth=HTTPBasicAuth(TW_USER, TW_PASSWORD),
            headers={"Content-Type": "application/json"}
        )

        value = r.json()["rows"][0]["OutboundCommand"]

        if value and value != "":
            print("Sende MQTT:", value)

            # Payload an MQTT Broker senden
            client.publish(MQTT_TOPIC, value)

            # Property zurücksetzen
            requests.put(
                f"{THINGWORX_URL}/Things/{THING_NAME}/Properties/OutboundCommand",
                auth=HTTPBasicAuth(TW_USER, TW_PASSWORD),
                headers={"Content-Type": "application/json"},
                json={"OutboundCommand": ""}
            )

    except Exception as e:
        print("Fehler:", e)

    time.sleep(1)
