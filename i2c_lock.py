from threading import Lock

# Shared lock for I2C bus access
i2c_lock = Lock()
