#!/usr/bin/env python3

# File:        io/buzzer.py
# By:          Samuel Duclos
# For:         My team.
# Description: Funky town with uARM buzzer.

import time

def play_funky_town(uarm=None, delay=5):
    uarm.set_servo_detach()
    time.sleep(1)
    uarm.set_buzzer(frequency=440, duration=0.125)
    uarm.set_buzzer(frequency=440, duration=0.125)
    uarm.set_buzzer(frequency=392, duration=0.125)
    uarm.set_buzzer(frequency=440, duration=0.125)
    time.sleep(0.5)
    uarm.set_buzzer(frequency=329.63, duration=0.25)
    time.sleep(0.5)
    uarm.set_buzzer(frequency=329.63, duration=0.125)
    uarm.set_buzzer(frequency=440, duration=0.125)
    uarm.set_buzzer(frequency=587.33, duration=0.125)
    uarm.set_buzzer(frequency=554.37, duration=0.125)
    uarm.set_buzzer(frequency=440, duration=0.125)
    time.sleep(0.125)
    time.sleep(delay)

