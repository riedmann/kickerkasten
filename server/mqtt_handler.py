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
    
    def __init__(self, broker="localhost", port=1883, client_id="kickerkasten", username=None, password=None, topic_prefix="kickerkasten"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
        
        # References to game components (set later)
        self.timer = None
        self.score_manager = None
        self.gpio_handler = None
        
        # MQTT topics
        self.topic_status = f"{topic_prefix}/status"
        self.topic_timer = f"{topic_prefix}/timer"
        self.topic_score = f"{topic_prefix}/score"
        self.topic_command = f"{topic_prefix}/command"
        
        # Background publishing thread
        self.publish_thread = None
        self.should_stop = threading.Event()
        
    def set_components(self, timer, score_manager, gpio_handler=None):
        """Set references to timer, score manager, and gpio handler"""
        self.timer = timer
        self.score_manager = score_manager
        self.gpio_handler = gpio_handler
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        print(f"[MQTT DEBUG] on_connect called with rc={rc}")
        if rc == 0:
            print(f"[MQTT] Connected to broker at {self.broker}:{self.port}")
            self.connected = True
            # Subscribe to command topic
            result = client.subscribe(self.topic_command)
            print(f"[MQTT] Subscribed to {self.topic_command} - Result: {result}")
            
            # Also subscribe to wildcard for debugging
            result2 = client.subscribe("edu/iot2021/#")
            print(f"[MQTT DEBUG] Also subscribed to edu/iot2021/# for debugging - Result: {result2}")
            
            print(f"[MQTT DEBUG] Subscription successful, waiting for messages...")
        else:
            print(f"[MQTT] Connection failed with code {rc}")
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        print(f"[MQTT] Disconnected from broker (code {rc})")
        self.connected = False
    
    def on_message(self, client, userdata, msg):
        """Callback when message received on subscribed topic"""
        print(f"[MQTT DEBUG] on_message called!")
        print(f"[MQTT DEBUG] Topic: {msg.topic}")
        print(f"[MQTT DEBUG] Payload (raw): {msg.payload}")
        try:
            payload = msg.payload.decode('utf-8')
            print(f"[MQTT] Received on {msg.topic}: {payload}")
            
            if msg.topic == self.topic_command:
                print(f"[MQTT DEBUG] Topic matches command topic, calling handle_command...")
                self.handle_command(payload)
            else:
                print(f"[MQTT DEBUG] Topic does not match. Expected: {self.topic_command}, Got: {msg.topic}")
        except Exception as e:
            print(f"[MQTT] Error processing message: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_command(self, command):
        """Handle incoming commands (supports both plain text and JSON)"""
        print(f"[MQTT DEBUG] handle_command called with: {command}")
        try:
            # Try to parse as JSON first
            try:
                print(f"[MQTT DEBUG] Attempting to parse as JSON...")
                data = json.loads(command)
                print(f"[MQTT DEBUG] JSON parsed successfully: {data}")
                # If JSON, extract command from "command" or "action" field
                cmd = data.get("command") or data.get("action") or data.get("cmd")
                print(f"[MQTT DEBUG] Extracted command from JSON: {cmd}")
                if cmd:
                    cmd = cmd.strip().lower()
                else:
                    print(f"[MQTT] JSON received but no command field found: {command}")
                    return
            except json.JSONDecodeError:
                # Not JSON, treat as plain text
                print(f"[MQTT DEBUG] Not JSON, treating as plain text")
                cmd = command.strip().lower()
            
            print(f"[MQTT DEBUG] Final command to execute: '{cmd}'")
            
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
            
            elif cmd == "ball":
                if self.gpio_handler:
                    from threading import Timer as ThreadingTimer
                    self.gpio_handler.ball_output.on()
                    ThreadingTimer(0.2, self.gpio_handler.ball_output.off).start()
                    print("[MQTT] Command: Ball out triggered")
            
            else:
                print(f"[MQTT] Unknown command: {cmd}")
        
        except Exception as e:
            print(f"[MQTT] Error handling command: {e}")
    
    def start(self):
        """Start MQTT client and background publishing"""
        try:
            print(f"[MQTT DEBUG] Starting MQTT handler...")
            print(f"[MQTT DEBUG] Broker: {self.broker}:{self.port}")
            print(f"[MQTT DEBUG] Client ID: {self.client_id}")
            print(f"[MQTT DEBUG] Username: {self.username}")
            print(f"[MQTT DEBUG] Command topic: {self.topic_command}")
            
            # Initialize MQTT client
            self.client = mqtt.Client(client_id=self.client_id)
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            print(f"[MQTT DEBUG] Callbacks registered")
            
            # Set username and password if provided
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
                print(f"[MQTT] Using authentication for user: {self.username}")
            
            # Connect to broker
            print(f"[MQTT] Connecting to {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, keepalive=60)
            print(f"[MQTT DEBUG] Connect called, waiting for on_connect callback...")
            
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
