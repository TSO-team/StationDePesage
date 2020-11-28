#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        Merge balance and use new CAN protocol.

import time
import pyuarm

sensor_threshold = 0.5
uart_delay = 2 # seconds
grab_delay = 5 # seconds
drop_delay = 5 # seconds
tty_name = 'USB0'

initial_position = {'x': 35.93, 'y': 124.12, 'z': 224.35, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 75.52, 'y': 280.37, 'z': 190.34, 'speed': 150, 'relative': False, 'wait': True}
drop_position = {'x': 73.87, 'y': 274.24, 'z': 210.05, 'speed': 150, 'relative': False, 'wait': True}

uarm = pyuarm.UArm(port_name='/dev/tty' + tty_name)
time.sleep(uart_delay)

def set_position(position, delay_0=1, delay_1=1, delay_2=1)
    uarm.set_servo_attach()
    time.sleep(delay_0)
    uarm.set_position(**position)
    time.sleep(delay_1)
    uarm.set_servo_detach()
    time.sleep(delay_2)

def set_pump(on=False, delay=1):
    uarm.set_pump(ON=on)
    time.sleep(delay)

CAN_protocol = CAN.Protocol(channel='socketcan', bustype='vcan0', arbitration_id=003, is_extended_id=False)
CAN_protocol.send(data=[0x40, 0xAA]) # Test with candump.

while True:
    set_position(initial_position)
    if CAN_protocol.condition_met():
        set_position(balance_position)
        if sensor.read_distance() < sensor_threshold:
            set_pump(on=True)
            buzzer.play_funky_town(uarm=uarm, delay=grab_delay)
            set_position(drop_position)
            set_pump(on=False)
            buzzer.play_funky_town(uarm=uarm, delay=drop_delay)

