#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: UARM control in Python for TSO_team.

#from communication.CAN.protocol import condition_met
from adafruit_extended_bus import ExtendedI2C as I2C

import time
import pyuarm
import busio
import adafruit_vl6180x

def read_vl6180x():
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
    print("Light (1x gain): {0}lux".format(light_lux))

# Create I2C bus.
i2c = I2C(1)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

initial_position = {'x': 35.93, 'y': 124.12, 'z': 224.35, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 75.52, 'y': 280.37, 'z': 190.34, 'speed': 150, 'relative': False, 'wait': True}
drop_position = {'x': 73.87, 'y': 274.24, 'z': 210.05, 'speed': 150, 'relative': False, 'wait': True}

uarm = pyuarm.UArm(port_name='/dev/ttyUSB0')

time.sleep(2)
uarm.set_servo_detach()

while True:
    uarm.set_position(**initial_position)
    #if condition_met():
    if True:
        uarm.set_servo_attach()
        uarm.set_position(**balance_position)
        read_vl6180x()
        uarm.set_pump(ON=True)
        uarm.set_buzzer(frequency=60, duration=1.5)
        time.sleep(5)
        uarm.set_position(**drop_position)
        uarm.set_pump(ON=False)
        uarm.set_buzzer(frequency=120, duration=1.5)
        uarm.set_servo_attach()
        time.sleep(5)
