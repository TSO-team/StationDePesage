#!/usr/bin/env python3

# File:        utils/buzzer.py
# By:          Samuel Duclos
# For:         My team.
# Description: Funky town with uARM buzzer.

import time

def play_funky_town(uarm=None, duration_multiplier=2.0, servo_detach_delay=2, transition_delay=5):
    uarm.set_servo_detach()
    time.sleep(servo_detach_delay)
    uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=98, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
    time.sleep(0.5 * duration_multiplier)
    uarm.set_buzzer(frequency=82.41, duration=0.25 * duration_multiplier)
    time.sleep(0.5 * duration_multiplier)
    uarm.set_buzzer(frequency=82.41, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=146.83, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=138.59, duration=0.125 * duration_multiplier)
    uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
    time.sleep(0.125 * duration_multiplier)
    time.sleep(transition_delay)

#def play_funky_town(uarm=None, delay=5):
#    uarm.set_buzzer(frequency=60, duration=1)

