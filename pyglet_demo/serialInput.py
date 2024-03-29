import serial
import struct
import sys
from os import system

BAUD_RATE = 115_200

DEV_FILE = "/dev/feather"


class Input:
    def __init__(
        self,
        on_green_trigger=None,
        on_red_trigger=None,
        on_green_hold=None,
        on_red_hold=None,
        on_battery_change=None,
    ):
        self.ser = serial.Serial(DEV_FILE, BAUD_RATE, timeout=0)
        self.on_green_trigger = self._check_and_call(on_green_trigger)
        self.on_red_trigger = self._check_and_call(on_red_trigger)
        self.on_battery_change = self._check_and_call(on_battery_change)
        self.on_green_hold = self._check_and_call(on_green_hold)
        self.on_red_hold = self._check_and_call(on_red_hold)

    def _check_and_call(self, callback):
        if callback is not None:
            return callback
        return lambda *args: None

    def update(self):
        data = self.ser.read(self.ser.in_waiting)
        if len(data) > 0:
            print(data, data[-1], len(data))
            last_byte = data[-1]
        if len(data) == 1:
            if last_byte == 0x10:
                self.on_green_trigger()
            elif last_byte == 0x20:
                self.on_red_trigger()
            elif last_byte == 0x40:
                self.on_red_hold()
            elif last_byte == 0x50:
                self.on_green_hold()
        elif len(data) == 5:
            if data[0] == 0x30:
                [battery_level] = struct.unpack("f", data[1:])
                self.on_battery_change(battery_level)
