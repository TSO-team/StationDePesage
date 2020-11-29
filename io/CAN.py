#!/usr/bin/env python3

# File:        io/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: TSO protocol for CAN bus.

from __future__ import print_function
import atexit, can, os, subprocess, time

channel = 'socketcan'
is_extended_id = False

class Protocol:
    def __init__(self, interface_type='vcan', arbitration_id=003, bitrate=50000, delay=1):
        self.arbitration_id = arbitration_id
        self.is_extended_id = is_extended_id
        self.interface_type = interface_type
        self.bustype = interface_type + str(0)
        self.delay = delay

        subprocess.run('modprobe vcan') # Ensure kernel modules are loaded.

        # Setup interface if it doesn't exist.
        if not os.path.exists('/sys/class/net/' + self.bustype):
            subprocess.run('ip link add dev ' + self.bustype + ' type ' + self.interface_type)

        # Virtual CAN interface has no bitrate.
        bitrate = ' bitrate ' + str(bitrate) if self.interface_type != 'vcan' else ''

        # Make sure the interface is up.
        subprocess.run('ip link set up ' + self.bustype + ' type ' + self.interface_type + bitrate)

        # Increase sending buffer size.
        subprocess.run('ifconfig ' + self.bustype + ' txqueuelen 1000')

        self.bus = can.interface.ThreadSafeBus(channel=channel, bustype=self.bustype)

    @atexit.register
    def __del__(self):
        subprocess.run('ip link set down ' + self.bustype)
        subprocess.run('ip link delete dev ' + self.bustype + ' type ' + self.interface_type)

    def send(self, data):
        msg = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.bus.send(msg)
            print('Message sent on {}.'.format(self.bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

        time.sleep(self.delay)

    def receive(self):
        try:
            msg = self.bus.recv(0.0) # Non-blocking read.

            if msg is not None:
                print('Message received on {}.'.format(self.bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

        return msg

    def condition_met(self):
        return True # Define this later...

