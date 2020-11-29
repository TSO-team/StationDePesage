#!/usr/bin/env python3

# File:        CAN_test.py
# By:          Samuel Duclos
# For:         My team.
# Description: CAN test in Python for TSO_team.

from __future__ import print_function
from .io import CAN

# Modifiable variables.
arbitration_id = 003
interface_type = 'vcan'
bitrate = 50000
CAN_delay = 1 # seconds

if __name__ == '__main__':
    TSO_protocol = CAN.Protocol(interface_type=interface_type, 
                                arbitration_id=arbitration_id, 
                                bitrate=bitrate, 
                                delay=CAN_delay)

    msg = [0x40, 0xAA]
    TSO_protocol.send(data=msg)

    msg = TSO_protocol.receive()
    if msg is not None:
        print(msg)

