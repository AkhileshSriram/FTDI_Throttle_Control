import serial
import time

def set_throttle(com_port, throttle_value):
    # Throttle value should be between 0 (off) and 65535 (full throttle)
    try:
        # Open serial port
        with serial.Serial(com_port, 115200, timeout=1) as ser:
            # Construct the command
            # Device ID is assumed to be 0 for simplicity
            command = bytearray([0x00, 0x80, (throttle_value >> 8) & 0xFF, throttle_value & 0xFF])
            # Calculate checksum
            checksum = 0 - sum(command) & 0xFF
            command.append(checksum)
            
            # Send command
            ser.write(command)
            # Wait for command to be processed
            time.sleep(0.1)
            
            print(f"Throttle set to {throttle_value}")
            
    except serial.SerialException as e:
        print(f"Failed to open serial port {com_port}: {e}")

if __name__ == "__main__":
    com_port = "COM11"  # Update this to the correct COM port
    throttle_value = 13107  # Mid-throttle example
    set_throttle(com_port, throttle_value)
