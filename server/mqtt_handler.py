"""
MQTT Handler for Kickerkasten
Publishes game state and accepts commands
"""
import paho.mqtt.client as mqtt
import json
import threading
from time import sleep


class MQTTHandler:
    """Handles MQTT communication for game state and commands"""
    
    def __init__(self, broker="localhost", port=1883, client_id="kickerkasten"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = None
        self.connected = False
        
        # References to game components (set later)
        self.timer = None
        self.score_manager = None
        
        # MQTT topics
        self.topic_status = "kickerkasten/status"
        self.topic_timer = "kickerkasten/timer"
        self.topic_score = "kickerkasten/score"
        self.topic_command = "kickerkasten/command"
        
        # Background publishing thread
        self.publish_thread = None
        self.should_stop = threading.Event()
        
    def set_components(self, timer, score_manager):
        """Set references to timer and score manager"""
        self.timer = timer
        self.score_manager = score_manager
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            print(f"[MQTT] Connected to broker at {self.broker}:{self.port}")
            self.connected = True
            # Subscribe to command topic
            client.subscribe(self.topic_command)
            print(f"[MQTT] Subscribed to {self.topic_command}")
        else:
            print(f"[MQTT] Connection failed with code {rc}")
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        print(f"[MQTT] Disconnected from broker (code {rc})")
        self.connected = False
    
    def on_message(self, client, userdata, msg):
        """Callback when message received on subscribed topic"""
        try:
            payload = msg.payload.decode('utf-8')
            print(f"[MQTT] Received on {msg.topic}: {payload}")
            
            if msg.topic == self.topic_command:
                self.handle_command(payload)
        except Exception as e:
            print(f"[MQTT] Error processing message: {e}")
    
    def handle_command(self, command):
        """Handle incoming commands"""
        try:
            cmd = command.strip().lower()
            
            if cmd == "start":
                if self.timer:
                    self.timer.start_timer()
                    print("[MQTT] Command: Start timer")
            
            elif cmd == "pause":
                if self.timer:
                    self.timer.pause_timer()
                    print("[MQTT] Command: Pause timer")
            
            elif cmd == "stop":
                if self.timer:
                    self.timer.stop_timer()
                    print("[MQTT] Command: Stop timer")
            
            elif cmd == "reset":
                if self.timer:
                    self.timer.reset_timer()
                    print("[MQTT] Command: Reset timer")
            
            else:
                print(f"[MQTT] Unknown command: {command}")
        
        except Exception as e:
            print(f"[MQTT] Error handling command: {e}")
    
    def start(self):
        """Start MQTT client and background publishing"""
        try:
            # Initialize MQTT client
            self.client = mqtt.Client(client_id=self.client_id)
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            # Connect to broker
            print(f"[MQTT] Connecting to {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, keepalive=60)
            
            # Start network loop in background
            self.client.loop_start()
            
            # Start publishing thread
            self.publish_thread = threading.Thread(target=self._publish_loop, daemon=True)
            self.publish_thread.start()
            
            print("[MQTT] Handler started")
            
        except Exception as e:
            print(f"[MQTT] Failed to start: {e}")
    
    def stop(self):
        """Stop MQTT client"""
        print("[MQTT] Stopping...")
        self.should_stop.set()
        
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
        
        if self.publish_thread:
            self.publish_thread.join(timeout=2.0)
    
    def _publish_loop(self):
        """Background thread that publishes state updates"""
        while not self.should_stop.is_set():
            try:
                if self.connected and self.timer and self.score_manager:
                    # Publish timer state
                    timer_data = self.timer.get_status()
                    self.publish_timer(timer_data)
                    
                    # Publish score
                    score_data = self.score_manager.get_score()
                    self.publish_score(score_data)
                    
                    # Publish combined status
                    status_data = {
                        "timer": timer_data,
                        "score": score_data
                    }
                    self.publish_status(status_data)
                
                # Publish every 1 second
                sleep(1.0)
                
            except Exception as e:
                print(f"[MQTT] Error in publish loop: {e}")
                sleep(1.0)
    
    def publish_timer(self, data):
        """Publish timer state"""
        if self.connected and self.client:
            payload = json.dumps(data)
            self.client.publish(self.topic_timer, payload, qos=0, retain=True)
    
    def publish_score(self, data):
        """Publish score state"""
        if self.connected and self.client:
            payload = json.dumps(data)
            self.client.publish(self.topic_score, payload, qos=0, retain=True)
    
    def publish_status(self, data):
        """Publish combined status"""
        if self.connected and self.client:
            payload = json.dumps(data)
            self.client.publish(self.topic_status, payload, qos=0, retain=True)
