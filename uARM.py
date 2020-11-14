# File:        algorithm.py
# By:          Samuel Duclos
# For:         My team.
# Description: Pseudocode for TSO_team.

from communication.CAN.protocol import condition_met
import pyuarm

balance_position = {'x': 0, 'y':, 0, 'z': 0, 'speed': 100}
drop_position = {'x': 100, 'y':, 100, 'z': 100, 'speed': 100}

arm = pyuarm.get_uarm()
arm.connect()

while True:
    arm.reset()
    while True:
        if condition_met():
            arm.set_position(**balance_position)
            arm.set_pump(True)
            arm.set_position(**drop_position)
            arm.set_pump(False)
