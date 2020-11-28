#!/usr/bin/env python3

# File:        io/sensor.py
# By:          Samuel Duclos
# For:         My team.
# Description: Time-of-Flight sensor control (attached to uARM tip).

from adafruit_extended_bus import ExtendedI2C as I2C

import time
import busio
import adafruit_vl6180x

i2c = I2C(1) # Create I2C bus.
sensor = adafruit_vl6180x.VL6180X(i2c) # Create sensor instance.

time.sleep(2)

def read_distance():
    range_mm = sensor.range
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
    light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
    #print("Light (1x gain): {0}lux".format(light_lux))
    return light_lux

