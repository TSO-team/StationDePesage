#!/usr/bin/env python3

# File:        utils/sensor.py
# By:          Samuel Duclos
# For:         My team.
# Description: Time-of-Flight sensor control (attached to uARM tip).

from __future__ import print_function
from adafruit_extended_bus import ExtendedI2C as I2C

import adafruit_vl6180x, busio, signal, time

class VL6180X:
    def __init__(self, i2c_port=1):
        i2c = I2C(i2c_port) # Create I2C bus.
        self.sensor = adafruit_vl6180x.VL6180X(i2c) # Create sensor instance.
        self.handle_exit_signals()
        time.sleep(2)

    def reset(self):
        print('Sensor closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

    def read_distance(self):
        range_mm = self.sensor.range
        print("Range: {0}mm".format(range_mm))
        # Read the light, note this requires specifying a gain value:
        # - adafruit_vl6180x.ALS_GAIN_1 = 1x
        # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
        # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
        # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
        # - adafruit_vl6180x.ALS_GAIN_5 = 5x
        # - adafruit_vl6180x.ALS_GAIN_10 = 10x
        # - adafruit_vl6180x.ALS_GAIN_20 = 20x
        # - adafruit_vl6180x.ALS_GAIN_40 = 40x
        light_lux = self.sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
        #print("Light (1x gain): {0}lux".format(light_lux))
        return light_lux

    def detect_object(self, sensor_threshold=0.5):
        return self.read_distance() < sensor_threshold
