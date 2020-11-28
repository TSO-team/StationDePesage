#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        Merge balance and use new CAN protocol.

bustype = 'vcan0'
arbitration_id = 003
sensor_threshold = 0.5
uart_delay, grab_delay, drop_delay, delay_0, delay_1, delay_2 = 2, 5, 5, 1, 1, 1 # seconds
uarm_tty_port = '/dev/ttyUSB0'
balance_tty_port = '/dev/ttyO3'

initial_position = {'x': 35.93, 'y': 124.12, 'z': 224.35, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 75.52, 'y': 280.37, 'z': 190.34, 'speed': 150, 'relative': False, 'wait': True}
vehicle_position = {'x': 73.87, 'y': 274.24, 'z': 210.05, 'speed': 150, 'relative': False, 'wait': True}

import time, pyuarm, subprocess
from .io import buzzer, CAN, sensor

uarm = pyuarm.UArm(port_name=uarm_tty_port)
time.sleep(uart_delay)

def set_position(position, delay_0=1, delay_1=1, delay_2=1)
    uarm.set_servo_attach()
    time.sleep(delay_0)
    uarm.set_position(**position)
    time.sleep(delay_1)
    uarm.set_servo_detach()
    time.sleep(delay_2)

def set_pump(on=False, pump_delay=1):
    uarm.set_pump(ON=on)
    time.sleep(pump_delay)

def grab(sensor_threshold=0.5, pump_delay=1, grab_delay=1):
    while not (sensor.read_distance() < sensor_threshold):
        set_pump(on=True, pump_delay=pump_delay)
        buzzer.play_funky_town(uarm=uarm, delay=grab_delay)

def drop(pump_delay=1, drop_delay=1):
    set_pump(on=False, pump_delay=pump_delay)
    buzzer.play_funky_town(uarm=uarm, delay=drop_delay)

def set_weight_somewhere(grab_position=None, 
                         drop_position=None, 
                         grab_delay=5, 
                         drop_delay=5, 
                         delay_0=1, 
                         delay_1=1, 
                         delay_2=1, 
                         sensor_threshold=0.5):
    set_position(grab_position, delay_0=1, delay_1=1, delay_2=1)
    grab(sensor_threshold=sensor_threshold, pump_delay=pump_delay, grab_delay=grab_delay)
    set_position(drop_position, delay_0=1, delay_1=1, delay_2=1)
    drop(pump_delay=1, drop_delay=1)
    set_position(initial_position, delay_0=delay_0, delay_1=delay_1, delay_2=delay_2)
    buzzer.play_funky_town(uarm=uarm, delay=drop_delay)

TSO_protocol = CAN.Protocol(bustype=bustype, arbitration_id=arbitration_id)
TSO_protocol.send(data=[0x40, 0xAA], delay=1) # Test with candump.
set_position(initial_position, delay_0=delay_0, delay_1=delay_1, delay_2=delay_2)
buzzer.play_funky_town(uarm=uarm, delay=drop_delay)

while True:
    if TSO_protocol.condition_met():
        set_weight_somewhere(grab_position=vehicle_position, 
                             drop_position=balance_position, 
                             grab_delay=grab_delay, 
                             drop_delay=drop_delay, 
                             delay_0=delay_0, 
                             delay_1=delay_1, 
                             delay_2=delay_2, 
                             sensor_threshold=sensor_threshold)
        subprocess.check_output("bash io/balance.sh " + balance_tty_port, stderr=subprocess.STDOUT, shell=True)
        set_weight_somewhere(grab_position=balance_position, 
                             drop_position=vehicle_position, 
                             grab_delay=grab_delay, 
                             drop_delay=drop_delay, 
                             delay_0=delay_0, 
                             delay_1=delay_1, 
                             delay_2=delay_2, 
                             sensor_threshold=sensor_threshold)

