#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.

import time
import pyuarm

from .sensor.VL6180X import read_distance
from .buzzer import funky_town
#from .communication.CAN.protocol import condition_met

sensor_threshold = 0.5

initial_position = {'x': 35.93, 'y': 124.12, 'z': 224.35, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 75.52, 'y': 280.37, 'z': 190.34, 'speed': 150, 'relative': False, 'wait': True}
drop_position = {'x': 73.87, 'y': 274.24, 'z': 210.05, 'speed': 150, 'relative': False, 'wait': True}

uarm = pyuarm.UArm(port_name='/dev/ttyUSB0')
time.sleep(2)

def set_position(position)
    uarm.set_servo_attach()
    time.sleep(1)
    uarm.set_position(**position)
    time.sleep(1)
    uarm.set_servo_detach()
    time.sleep(1)

def set_pump(on=False):
    uarm.set_pump(ON=on)
    time.sleep(1)

while True:
    set_position(initial_position)
    #if condition_met():
    if True:
        set_position(balance_position)
        if read_distance() < sensor_threshold:
            set_pump(on=True)
            funky_town(uarm=uarm)
            time.sleep(5)
            set_position(drop_position)
            set_pump(on=False)
            funky_town(uarm=uarm)
            time.sleep(5)
