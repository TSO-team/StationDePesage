#!/usr/bin/env python3

# File:        utils/buzzer.py
# By:          Samuel Duclos
# For:         My team.
# Description: Funky town with uARM buzzer.

import signal, time

class Buzzer:
    def __init__(self, uarm=None, servo_detach_delay=5, transition_delay=5):
        self.uarm = uarm
        self.servo_detach_delay = servo_detach_delay
        self.transition_delay = transition_delay
        self.handle_exit_signals()

    def set_servo_detach(self):
        self.uarm.set_servo_detach()
        time.sleep(self.servo_detach_delay)

    def play_funky_town(self, duration_multiplier=2.5):
        self.set_servo_detach()
        self.uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=98, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
        time.sleep(0.5 * duration_multiplier)
        self.uarm.set_buzzer(frequency=82.41, duration=0.25 * duration_multiplier)
        time.sleep(0.5 * duration_multiplier)
        self.uarm.set_buzzer(frequency=82.41, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=146.83, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=138.59, duration=0.125 * duration_multiplier)
        self.uarm.set_buzzer(frequency=110, duration=0.125 * duration_multiplier)
        time.sleep(0.125 * duration_multiplier)
        time.sleep(self.transition_delay)

    def reset(self):
        print('Buzzer closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

#def play_funky_town(uarm=None, delay=5):
#    uarm.set_buzzer(frequency=60, duration=1)

