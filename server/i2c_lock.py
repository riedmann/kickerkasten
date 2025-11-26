"""
Shared I2C lock to prevent bus contention between displays
"""
from threading import Lock

# Global lock for all I2C operations
i2c_lock = Lock()
