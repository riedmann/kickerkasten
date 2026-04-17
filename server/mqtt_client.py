# mqtt_client.py
import paho.mqtt.client as mqtt
import json
import os
import socket
import time
import threading

# Broker-Konfiguration – am besten über Umgebungsvariablen setzen
BROKER = os.getenv("MQTT_BROKER", "letto.htlwrn.ac.at")
PORT = int(os.getenv("MQTT_PORT", 1883))
USERNAME = os.getenv("MQTT_USER", "iot2021")
PASSWORD = os.getenv("MQTT_PASS", "iot2021")
BASE_TOPIC = os.getenv("MQTT_BASE_TOPIC", "kickerkasten")

# Optional: setze client id so, dass mehrere Geräte keinen Konflikt erzeugen
CLIENT_ID = f"kickerkasten-{socket.gethostname()}"

# QoS & retain standard
QOS = 1
RETAIN = False

class MQTTClient:
    def __init__(self, broker=BROKER, port=PORT, username=USERNAME, password=PASSWORD, client_id=CLIENT_ID):
        self.broker = broker
        self.port = port
        self.client_id = client_id

        self._client = mqtt.Client(client_id=self.client_id, clean_session=True)
        if username and password:
            self._client.username_pw_set(username, password)

        # Callbacks
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_log = self._on_log

        self._connected = threading.Event()
        self._should_stop = False

        # Last Will (optional): signalisiert Verbindungsverlust
        will_topic = f"{BASE_TOPIC}/status/{self.client_id}"
        self._client.will_set(will_topic, json.dumps({"status": "offline"}), qos=1, retain=True)

        # Start connection (non-blocking)
        self._connect_loop_thread = threading.Thread(target=self._connect_loop, daemon=True)
        self._connect_loop_thread.start()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] verbunden mit", self.broker)
            # Optional: veröffentliche online-Status
            self._client.publish(f"{BASE_TOPIC}/status/{self.client_id}", json.dumps({"status": "online"}), qos=1, retain=True)
            self._connected.set()
        else:
            print("[MQTT] Verbindungsfehler rc=", rc)

    def _on_disconnect(self, client, userdata, rc):
        print("[MQTT] getrennt, rc=", rc)
        self._connected.clear()

    def _on_log(self, client, userdata, level, buf):
        # Nur für Debug; kannst du weglassen oder filtern
        # print("[MQTT LOG]", buf)
        pass

    def _connect_loop(self):
        """Versucht permanent, eine Verbindung zum Broker aufzubauen und zu halten."""
        while not self._should_stop:
            try:
                if not self._connected.is_set():
                    print(f"[MQTT] Versuche Verbindung zu {self.broker}:{self.port} ...")
                    # connect() ist nicht-blockierend, loop_start hält Hintergrund-IO
                    self._client.connect(self.broker, self.port, keepalive=60)
                    self._client.loop_start()
                # Warte etwas bevor erneuter Versuch
                time.sleep(5)
            except Exception as e:
                print("[MQTT] Connect-Loop Fehler:", e)
                try:
                    self._client.loop_stop()
                except:
                    pass
                time.sleep(5)

    def publish_score(self, score: dict):
        """Score ist z.B. {'team_left': 2, 'team_right': 1}"""
        topic = f"{BASE_TOPIC}/score"
        payload = json.dumps(score)
        try:
            self._client.publish(topic, payload, qos=QOS, retain=RETAIN)
            # Optionaler Log
            print(f"[MQTT] published to {topic}: {payload}")
        except Exception as e:
            print("[MQTT] publish_score error:", e)

    def publish_timer(self, timer_status: dict):
        """timer_status z.B. aus timer.get_status()"""
        topic = f"{BASE_TOPIC}/timer"
        payload = json.dumps(timer_status)
        try:
            self._client.publish(topic, payload, qos=QOS, retain=RETAIN)
            print(f"[MQTT] published to {topic}: {payload}")
        except Exception as e:
            print("[MQTT] publish_timer error:", e)

    def publish_event(self, event_name: str, data=None):
        topic = f"{BASE_TOPIC}/event"
        payload = json.dumps({"event": event_name, "data": data})
        try:
            self._client.publish(topic, payload, qos=QOS, retain=False)
            print(f"[MQTT] published event {event_name}: {payload}")
        except Exception as e:
            print("[MQTT] publish_event error:", e)

    def stop(self):
        self._should_stop = True
        try:
            self._client.publish(f"{BASE_TOPIC}/status/{self.client_id}", json.dumps({"status": "offline"}), qos=1, retain=True)
            self._client.loop_stop()
            self._client.disconnect()
        except Exception as e:
            print("[MQTT] stop error:", e)
