import numpy as np
import serial  # You need to install pySerial to use this

class SerialLink():
    def __init__(self, serial_port, device_id):
        self.serial_link = serial.Serial(serial_port, 115200)
        self.device_id = device_id
        self.register_dictionary = {
            "read": {
                "throttle": 3,
                "speed": 5,
                "power": 4,
            },
            "write": {
                "throttle": 128,
                "e_stop": 130,
            }
        }
        self.scale_dictionary = {
            "throttle": 1.0,
            "speed": 20416.66,
            "power": 0.2502,
        }

    def calc_checksum(self, cmd):
        return (0 - sum(cmd)) % 256

    def write_command(self, command):
        self.serial_link.write(command)
        response = self.serial_link.read(3)  # Read the response which is 3 bytes long
        return response

    def write_throttle(self, value):
        command = [128 + self.device_id, self.register_dictionary["write"]["throttle"], value >> 8, value & 0xFF]
        command.append(self.calc_checksum(command))
        return self.write_command(command)
    
    

    def emergency_stop(self, activate=True):
        value = 1 if activate else 0
        command = [128 + self.device_id, self.register_dictionary["write"]["e_stop"], 0, value]
        command.append(self.calc_checksum(command))
        return self.write_command(command)

    def read_var(self, var):
        if var not in self.register_dictionary["read"]:
            raise ValueError("Variable not available for reading")
        register = self.register_dictionary["read"][var]
        command = [128 + self.device_id, register, 0, 0]
        command.append(self.calc_checksum(command))
        response = self.write_command(command)
        if len(response) == 3:
            value = (response[0] << 8) + response[1]
            scale = self.scale_dictionary[var]
            return value * scale / 2042.0
        else:
            raise Exception("Invalid response from serial link")
