#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        Verify/test CAN protocol is all implemented.
#              Parse balance output correctly and output weight to CAN after dividing.

from __future__ import print_function
from utils import balance, buzzer, CAN, sensor
import pyuarm, time

CAN_interface_type = 'vcan'
CAN_ID = 3
CAN_bitrate = 50000
CAN_time_base = 0.02 # 20 milliseconds between each station.
uarm_tty_port = '/dev/ttyUSB1'
balance_tty_port = '/dev/ttyUSB0'
sensor_port = 1
sensor_threshold = 0.5
buzzer_duration_multiplier = 2.0
uart_delay, grab_delay, drop_delay, pump_delay, CAN_delay = 2, 5, 5, 2, 2 # seconds
servo_detach_delay, delay_0, delay_1, delay_2, delay = 2, 2, 2, 2, 5 # seconds

initial_position = {'x': 21.6, 'y': 80.79, 'z': 186.11, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 313.93, 'y': 18.76, 'z': 178.67, 'speed': 150, 'relative': False, 'wait': True}
vehicle_position = {'x': -232.97, 'y': 120.86, 'z': 126.59, 'speed': 150, 'relative': False, 'wait': True}

uarm = pyuarm.UArm(port_name=uarm_tty_port)
time.sleep(uart_delay)

sensor = sensor.VL6180X(i2c_port=i2c_port)
balance = balance.Balance(tty_port=balance_tty_port)

def set_position(position, delay_0=1, delay_1=1, delay_2=1):
    uarm.set_servo_attach()
    time.sleep(delay_0)
    uarm.set_position(**position)
    time.sleep(delay_1)
    uarm.set_servo_detach()
    time.sleep(delay_2)

def set_pump(on=False, pump_delay=1):
    uarm.set_pump(ON=on)
    time.sleep(pump_delay)

def grab(uarm=None, 
         grab_position=None, 
         sensor_threshold=0.5, 
         pump_delay=1, 
         grab_delay=1, 
         delay_0=1, 
         delay_1=1, 
         delay_2=1):
    set_position(position=grab_position, delay_0=delay_0, delay_1=delay_1, delay_2=delay_2)
    while not sensor.detect_object(sensor_threshold=sensor_threshold):
        set_pump(on=True, pump_delay=pump_delay)
        buzzer.play_funky_town(uarm=uarm, duration_multiplier=buzzer_duration_multiplier, servo_detach_delay=servo_detach_delay, transition_delay=grab_delay)

def drop(uarm=None, drop_position=None, pump_delay=1, drop_delay=1, delay_0=1, delay_1=1, delay_2=1):
    set_position(position=drop_position, delay_0=delay_0, delay_1=delay_1, delay_2=delay_2)
    set_pump(on=False, pump_delay=pump_delay)
    buzzer.play_funky_town(uarm=uarm, duration_multiplier=buzzer_duration_multiplier, servo_detach_delay=servo_detach_delay, transition_delay=drop_delay)

def return_to_initial_position(uarm=None, position=None, delay_0=1, delay_1=1, delay_2=1, delay=5):
    set_position(position=initial_position, delay_0=delay_0, delay_1=delay_1, delay_2=delay_2)
    buzzer.play_funky_town(uarm=uarm, duration_multiplier=buzzer_duration_multiplier, servo_detach_delay=servo_detach_delay, transition_delay=drop_delay)

def set_weight_somewhere(uarm=None, 
                         grab_position=None, 
                         drop_position=None, 
                         grab_delay=5, 
                         drop_delay=5, 
                         pump_delay=1, 
                         delay_0=1, 
                         delay_1=1, 
                         delay_2=1, 
                         delay=1, 
                         sensor_threshold=0.5):

    grab(uarm=uarm, 
         grab_position=grab_position, 
         sensor_threshold=sensor_threshold, 
         pump_delay=pump_delay, 
         grab_delay=grab_delay, 
         delay_0=delay_0, 
         delay_1=delay_1, 
         delay_2=delay_2)

    drop(uarm=uarm, 
         drop_position=drop_position, 
         pump_delay=pump_delay, 
         drop_delay=drop_delay, 
         delay_0=delay_0, 
         delay_1=delay_1, 
         delay_2=delay_2)

    return_to_initial_position(uarm=uarm, 
                               position=initial_position, 
                               delay_0=delay_0, 
                               delay_1=delay_1, 
                               delay_2=delay_2, 
                               delay=delay)

TSO_protocol = CAN.Protocol(interface_type=CAN_interface_type, 
                            arbitration_id=CAN_ID, 
                            bitrate=CAN_bitrate, 
                            time_base=CAN_time_base, 
                            delay=CAN_delay)

return_to_initial_position(uarm=uarm, 
                           position=initial_position, 
                           delay_0=delay_0, 
                           delay_1=delay_1, 
                           delay_2=delay_2, 
                           delay=delay)

while True:
    if TSO_protocol.condition_met():
        set_weight_somewhere(uarm=uarm, 
                             grab_position=vehicle_position, 
                             drop_position=balance_position, 
                             grab_delay=grab_delay, 
                             drop_delay=drop_delay, 
                             pump_delay=pump_delay, 
                             delay_0=delay_0, 
                             delay_1=delay_1, 
                             delay_2=delay_2, 
                             delay=delay, 
                             sensor_threshold=sensor_threshold)

        msg = balance.weigh()
        TSO_protocol.send(msg)

        set_weight_somewhere(uarm=uarm, 
                             grab_position=balance_position, 
                             drop_position=vehicle_position, 
                             grab_delay=grab_delay, 
                             drop_delay=drop_delay, 
                             pump_delay=pump_delay, 
                             delay_0=delay_0, 
                             delay_1=delay_1, 
                             delay_2=delay_2, 
                             delay=delay, 
                             sensor_threshold=sensor_threshold)

