#!/usr/bin/env python3

# File:        utils/buzzer.py
# By:          Samuel Duclos
# For:         My team.
# Description: Funky town with uARM buzzer.

import time

'''
def play_funky_town(uarm=None, delay=5):
    uarm.set_servo_detach()
    time.sleep(2)
    uarm.set_buzzer(frequency=440, duration=0.25)
    uarm.set_buzzer(frequency=440, duration=0.25)
    uarm.set_buzzer(frequency=392, duration=0.25)
    uarm.set_buzzer(frequency=440, duration=0.25)
    time.sleep(1.0)
    uarm.set_buzzer(frequency=329.63, duration=0.5)
    time.sleep(1.0)
    uarm.set_buzzer(frequency=329.63, duration=0.25)
    uarm.set_buzzer(frequency=440, duration=0.25)
    uarm.set_buzzer(frequency=587.33, duration=0.25)
    uarm.set_buzzer(frequency=554.37, duration=0.25)
    uarm.set_buzzer(frequency=440, duration=0.25)
    time.sleep(0.25)
    time.sleep(delay)
'''

def play_funky_town(uarm=None, delay=5):
    uarm.set_buzzer(frequency=60, duration=1)
