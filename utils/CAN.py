#!/usr/bin/env python3

# File:        utils/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: TSO protocol for CAN bus.

from __future__ import print_function
import can, os, signal, subprocess, time

channel = 'socketcan'
is_extended_id = False

class Protocol:
    def __init__(self, interface_type='vcan', arbitration_id=3, bitrate=50000, delay=1):
        self.arbitration_id = arbitration_id
        self.is_extended_id = is_extended_id
        self.interface_type = interface_type
        self.bustype = interface_type + str(0)
        self.delay = delay

        signal.signal(signal.SIGINT, self.__del__) # Handle exits for clean up.

        subprocess.run('/sbin/modprobe vcan', shell=True, check=True) # Ensure kernel modules are loaded.

        # Setup interface if it doesn't exist.
        if not os.path.exists('/sys/class/net/' + self.bustype):
            subprocess.run('/sbin/ip link add dev ' + self.bustype + ' type ' + self.interface_type, shell=True, check=True)

        # Virtual CAN interface has no bitrate.
        bitrate = ' bitrate ' + str(bitrate) if self.interface_type != 'vcan' else ''

        # Make sure the interface is up.
        subprocess.run('/sbin/ip link set up ' + self.bustype + ' type ' + self.interface_type + bitrate, 
                       shell=True, check=True)

        # Increase sending buffer size.
        subprocess.run('/sbin/ifconfig ' + self.bustype + ' txqueuelen 1000', shell=True, check=True)

        self.bus = can.interface.ThreadSafeBus(channel=channel, bustype=self.bustype)

    def __del__(self):
        subprocess.run('/sbin/ip link set down ' + self.bustype)
        subprocess.run('/sbin/ip link delete dev ' + self.bustype + ' type ' + self.interface_type)

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

