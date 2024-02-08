import serial
import time

def set_throttle(com_port, throttle_value, duration, interval=0.1):
    """
    Sets the throttle for a specified duration.

    Args:
    com_port (str): The COM port to use.
    throttle_value (int): The throttle value to set, scaled 0 to 65535.
    duration (float): How long to maintain the throttle (in seconds).
    interval (float): How often to send the throttle command (in seconds).
    """
    end_time = time.time() + duration
    try:
        with serial.Serial(com_port, 115200, timeout=1) as ser:
            while time.time() < end_time:
                # Assuming Device ID is 0 and register for throttle is 128
                command = bytearray([0x80, 128, (throttle_value >> 8) & 0xFF, throttle_value & 0xFF])
                checksum = (0 - sum(command)) & 0xFF
                command.append(checksum)
                
                ser.write(command)
                time.sleep(interval)  # Wait before sending the next command
                
                print(f"Throttle set to {throttle_value}")
    except serial.SerialException as e:
        print(f"Failed to open serial port {com_port}: {e}")

if __name__ == "__main__":
    com_port = "COM3"  # Update to your COM port
    throttle_value = 0  # Mid-range example throttle value
    duration = 10  # Maintain throttle for 10 seconds
    set_throttle(com_port, throttle_value, duration)
