#!/usr/bin/env python3

# File:        python/utils/uarm.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        Fix scan()

from __future__ import print_function
import pyuarm, signal, time

initial_position = {'x': 21.6, 'y': 80.79, 'z': 186.11, 'speed': 150, 'relative': False, 'wait': True}

class UARM:
    def __init__(self, uarm_tty_port='/dev/ttyUSB1', uart_delay=2, initial_position=initial_position, servo_attach_delay=5, set_position_delay=5, servo_detach_delay=5, pump_delay=5):
        self.uarm_tty_port = uarm_tty_port
        self.uart_delay = uart_delay
        self.initial_position = initial_position
        self.servo_attach_delay = servo_attach_delay
        self.set_position_delay = set_position_delay
        self.servo_detach_delay = servo_detach_delay
        self.pump_delay = pump_delay
        self.uarm = pyuarm.UArm(port_name=self.uarm_tty_port)
        self.handle_exit_signals()
        time.sleep(self.uart_delay)

    def set_servo_attach(self):
        self.uarm.set_servo_attach()
        time.sleep(self.servo_attach_delay)

    def set_servo_detach(self):
        self.uarm.set_servo_detach()
        time.sleep(self.servo_detach_delay)

    def set_position(self, position=None):
        self.set_servo_attach()
        self.uarm.set_position(**position)
        time.sleep(self.set_position_delay)
        self.set_servo_detach()

    def set_pump(self, on=False):
        self.set_servo_attach()
        self.uarm.set_pump(ON=on)
        time.sleep(self.pump_delay)
        self.set_servo_detach()

    def grab(self, grab_position=None, sensor=None, sensor_threshold=0.5):
        self.set_position(position=grab_position)
        while not self.sensor.detect_object(sensor_threshold=sensor_threshold):
            self.set_pump(on=True)

    def drop(self, drop_position=None):
        self.set_position(position=drop_position)
        self.set_pump(on=False)

    # Fix me.
    def scan(self, sensor=None, sensor_threshold=0.5):
        is_breaking = False
        relative_x = int((0 - args.stride_x) / 2) * args.scan_x_displacement
        relative_y = int((0 - args.stride_y) / 2) * args.scan_y_displacement
        relative_z = int((0 - args.stride_z) / 2) * args.scan_z_displacement
        position = {'x': relative_x, 'y': relative_y, 'z': relative_z, 'speed': args.speed, 'relative': True, 'wait': True}
        uarm.set_position(position)

        for k in range(0, args.scan_z_displacement, args.stride_z):
            for j in range(0, args.scan_y_displacement, args.stride_y):
                for i in range(0, args.scan_x_displacement, args.stride_x):
                    position = {'x': i, 'y': j, 'z': k, 'speed': args.speed, 'relative': True, 'wait': True}
                        uarm.grab(grab_position=position, sensor=sensor, sensor_threshold=sensor_threshold)
                    if is_breaking:
                        break
                if is_breaking:
                    break

    def reset(self):
        self.set_pump(on=False)
        self.set_position(position=self.initial_position)
        self.set_servo_detach()
        print('uARM closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles disconnected TTY for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

    def set_weight_to_somewhere(self, grab_position=None, sensor=sensor, drop_position=None, sensor_threshold=0.5):
        self.grab(grab_position=grab_position, sensor=sensor, sensor_threshold=sensor_threshold)
        self.drop(drop_position=drop_position)
        self.reset()

