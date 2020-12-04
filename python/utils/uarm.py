#!/usr/bin/env python3

# File:        utils/uarm.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.

from __future__ import print_function
import pyuarm, time

initial_position = {'x': 21.6, 'y': 80.79, 'z': 186.11, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 313.93, 'y': 18.76, 'z': 178.67, 'speed': 150, 'relative': False, 'wait': True}
vehicle_position = {'x': -232.97, 'y': 120.86, 'z': 126.59, 'speed': 150, 'relative': False, 'wait': True}

class UARM:
    def __init__(self, uarm_tty_port='/dev/ttyUSB1', uart_delay=2, initial_position=None, servo_attach_delay=5, set_position_delay=5, servo_detach_delay=5, pump_delay=5):
        self.uarm_tty_port = uarm_tty_port
        self.uart_delay = uart_delay
        self.initial_position = initial_position
        self.servo_attach_delay = servo_attach_delay
        self.set_position_delay = set_position_delay
        self.servo_detach_delay = servo_detach_delay
        self.pump_delay = pump_delay
        self.uarm = pyuarm.UArm(port_name=self.uarm_tty_port)
        time.sleep(self.uart_delay)

    def set_position(self, position=None):
        self.uarm.set_servo_attach()
        time.sleep(self.servo_attach_delay)
        self.uarm.set_position(**position)
        time.sleep(self.set_position_delay)
        self.uarm.set_servo_detach()
        time.sleep(self.servo_detach_delay)

    def set_pump(self, on=False):
        self.uarm.set_pump(ON=on)
        time.sleep(self.pump_delay)

    def grab(self, grab_position=None, sensor=None, sensor_threshold=0.5):
        self.set_position(position=grab_position)
        while not self.sensor.detect_object(sensor_threshold=sensor_threshold):
            self.set_pump(on=True)

    def drop(self, drop_position=None):
        self.set_position(position=drop_position)
        self.set_pump(on=False)

    def return_to_initial_position(self):
        set_position(position=self.initial_position)

    def set_weight_somewhere(self, grab_position=None, drop_position=None, sensor_threshold=0.5):
        self.grab(grab_position=grab_position, sensor=sensor, sensor_threshold=sensor_threshold)
        self.drop(drop_position=drop_position)
        self.return_to_initial_position()

