import serial
import time

def set_and_read_throttle(com_port, throttle_value, duration, interval=0.5):
    end_time = time.time() + duration
    with serial.Serial(com_port, 115200, timeout=1) as ser:
        while time.time() < end_time:
            # Write to throttle register
            write_command = bytearray([0x80, 0x80, (throttle_value >> 8) & 0xFF, throttle_value & 0xFF])
            write_checksum = (0 - sum(write_command)) & 0xFF
            write_command.append(write_checksum)
            
            ser.write(write_command)
            print(f"Sent throttle set command: {write_command.hex()}")

            time.sleep(interval)

            # Read from throttle register
            read_command = bytearray([0x80, 0x03, 0x00, 0x00])
            read_checksum = (0 - sum(read_command)) & 0xFF
            read_command.append(read_checksum)
            
            ser.write(read_command)
            response = ser.read(3)
            
            if len(response) == 3:
                # Assuming the first byte is not part of the throttle value
                throttle_response = (response[0] << 8) + response[1]
                print(f"Throttle read value: {throttle_response}")
            else:
                print("Invalid response length or communication error")

            time.sleep(interval)

if __name__ == "__main__":
    com_port = "COM3"  # Update to your COM port
    throttle_value = 15000  # Adjust according to your needs
    duration = 10  # Duration to perform the throttle read/write
    set_and_read_throttle(com_port, throttle_value, duration)
