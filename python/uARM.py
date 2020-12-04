#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        Verify/test CAN protocol is all implemented.
#              Parse balance output correctly and output weight to CAN after dividing.

from __future__ import print_function
from utils import balance, buzzer, CAN, sensor, uarm
import time

CAN_interface_type = 'vcan'
CAN_ID = 3
CAN_bitrate = 50000
CAN_time_base = 0.02 # 20 milliseconds between each station.
uarm_tty_port = '/dev/ttyUSB1'
balance_tty_port = '/dev/ttyUSB0'
sensor_port = 1
sensor_threshold = 0.5
buzzer_duration_multiplier = 2.5
uart_delay, grab_delay, drop_delay, pump_delay, CAN_delay = 2, 5, 5, 5, 2 # seconds
servo_attach_delay, set_position_delay, servo_detach_delay, transition_delay = 5, 5, 5, 5 # seconds

initial_position = {'x': 21.6, 'y': 80.79, 'z': 186.11, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 313.93, 'y': 18.76, 'z': 178.67, 'speed': 150, 'relative': False, 'wait': True}
vehicle_position = {'x': -232.97, 'y': 120.86, 'z': 126.59, 'speed': 150, 'relative': False, 'wait': True}

uarm = uarm.UARM(uarm_tty_port='/dev/ttyUSB1', 
                 uart_delay=uart_delay, 
                 initial_position=initial_position, 
                 servo_attach_delay=servo_attach_delay, 
                 set_position_delay=set_position_delay, 
                 servo_detach_delay=servo_detach_delay, 
                 pump_delay=pump_delay)

buzzer = buzzer.Buzzer(uarm=uarm.uarm, servo_detach_delay=uarm.servo_detach_delay, transition_delay=transition_delay)
sensor = sensor.VL6180X(i2c_port=i2c_port)
balance = balance.Balance(tty_port=balance_tty_port)

TSO_protocol = CAN.Protocol(interface_type=CAN_interface_type, 
                            arbitration_id=CAN_ID, 
                            bitrate=CAN_bitrate, 
                            time_base=CAN_time_base, 
                            delay=CAN_delay)

uarm.reset()

while True:
    if TSO_protocol.condition_met():
        uarm.set_weight_to_somewhere(grab_position=vehicle_position, drop_position=balance_position, sensor=sensor, sensor_threshold=sensor_threshold)
        msg = balance.weigh()
        TSO_protocol.send(msg)
        buzzer.play_funky_town(duration_multiplier=buzzer_duration_multiplier)
        uarm.set_weight_to_somewhere(grab_position=balance_position, drop_position=vehicle_position, sensor=sensor, sensor_threshold=sensor_threshold)
        buzzer.play_funky_town(duration_multiplier=buzzer_duration_multiplier)

