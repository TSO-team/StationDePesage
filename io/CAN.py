#!/usr/bin/env python3

# File:        io/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: Funky town with uARM buzzer.

import time
import can


class Protocol:
    def __init__(self, channel='socketcan', bustype='vcan0', arbitration_id=003, is_extended_id=False):
        self.arbitration_id = arbitration_id
        self.is_extended_id = is_extended_id
        self.bus = can.interface.ThreadSafeBus(channel=channel, bustype=bustype)

    def set_message(self, data):
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

    def send(self, data, delay=1):
        self.set_message(data=data)
        bus.send(self.msg)
        time.sleep(delay)

    def condition_met(self):
        return True # Define this later...

