import serial
from SerialLink import SerialLink


serial_port = 'COM11'  # This will vary depending on your system
device_id = 0
link = SerialLink(serial_port, device_id)

# Write throttle command
throttle_value = 13107  # Mid-point value for demonstration
link.write_throttle(throttle_value)

# Read throttle, speed, and power
throttle = link.read_var("throttle")
speed = link.read_var("speed")
power = link.read_var("power")

print(f"Throttle: {throttle}ms, Speed: {speed} RPM, Power: {power}%")

# Activate emergency stop
#link.emergency_stop(True)