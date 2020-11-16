#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: UARM control in Python for TSO_team.

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import os, sys, time
from uf.wrapper.uarm_api import UarmAPI
from uf.utils.log import *
from communication.CAN.protocol import condition_met

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

balance_position = {'x': 0, 'y': 0, 'z': 0, 'speed': 100, 'relative': False, 'wait': True}
drop_position = {'x': 190, 'y': 0, 'z': 150, 'speed': 100, 'relative': False, 'wait': True}

#uarm = UarmAPI(dev_port='/dev/ttyUSB0')
uarm = UarmAPI(filters={'hwid': 'USB VID:PID=0403:6001'}) # Default filter.

time.sleep(2)
print(uarm.get_device_info())

while True:
    uarm.reset()
    if condition_met():
        uarm.set_position(**balance_position)
        uarm.set_pump(on=True)
        uarm.set_buzzer()
        uarm.set_position(**drop_position)
        uarm.set_pump(on=False)
        uarm.set_buzzer()
