import board
import busio
from adafruit_ht16k33 import segments

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create display objects for both goal displays
display1 = segments.Seg7x4(i2c, address=0x74)  # SEVEN_SEGMENT_ADDRESS_GOALS_1
display2 = segments.Seg7x4(i2c, address=0x72)  # SEVEN_SEGMENT_ADDRESS_GOALS_2

# Clear displays
display1.fill(0)
display2.fill(0)

# Display numbers
display1.print("12")  # Goals for team 1
display1.colon = True  # Show colon separator

display2.print("34")  # Goals for team 2
display2.colon = True  # Show colon separator
