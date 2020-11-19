#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: UARM control in Python for TSO_team.

import time
import pyuarm
#from communication.CAN.protocol import condition_met

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

initial_position = {'x': 35.93, 'y': 124.12, 'z': 224.35, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 75.52, 'y': 280.37, 'z': 190.34, 'speed': 150, 'relative': False, 'wait': True}
drop_position = {'x': 73.87, 'y': 274.24, 'z': 210.05, 'speed': 150, 'relative': False, 'wait': True}

uarm = pyuarm.UArm(port_name='/dev/ttyUSB0')

time.sleep(2)
uarm.set_servo_detach()

while True:
    uarm.set_position(**initial_position)
    #if condition_met():
    if True:
        uarm.set_servo_attach()
        uarm.set_position(**balance_position)
        uarm.set_pump(ON=True)
        uarm.set_buzzer(frequency=60, duration=1.5)
        time.sleep(5)
        uarm.set_position(**drop_position)
        uarm.set_pump(ON=False)
        uarm.set_buzzer(frequency=120, duration=1.5)
        uarm.set_servo_attach()
        time.sleep(5)
