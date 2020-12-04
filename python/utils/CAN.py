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
    def __init__(self, interface_type='vcan', arbitration_id=3, bitrate=50000, time_base=0.02, delay=1):
        self.arbitration_id = arbitration_id
        self.is_extended_id = is_extended_id
        self.interface_type = interface_type
        self.interface = interface_type + str(0)
        self.time_base = time_base
        self.delay = delay

        # Virtual CAN interface has no bitrate.
        if self.interface_type != 'vcan':
            bitrate = ' bitrate ' + str(bitrate)
            self.bustype = self.interface
        else:
            self.bustype = 'virtual'

        self.handle_exit_signals()
        self.pre_configure_CAN(bitrate=bitrate)

        self.sending_bus = can.interface.Bus(channel=channel, bustype=self.bustype)
        self.receiving_bus = can.interface.Bus(channel=channel, bustype=self.bustype)

    def reset(self):
        subprocess.run('/sbin/ip link set down ' + self.interface, shell=True, check=True)
        subprocess.run('/sbin/ip link delete dev ' + self.interface + ' type ' + self.interface_type, shell=True, check=True)
        print('CAN closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

    def pre_configure_CAN(self, bitrate=50000):
        subprocess.run('/sbin/modprobe vcan', shell=True, check=True) # Ensure kernel modules are loaded.

        # Setup interface if it doesn't exist.
        if not os.path.exists('/sys/class/net/' + self.interface):
            subprocess.run('/sbin/ip link add dev ' + self.interface + ' type ' + self.interface_type, shell=True, check=True)

        # Make sure the interface is up.
        subprocess.run('/sbin/ip link set up ' + self.interface + ' type ' + self.interface_type + bitrate, shell=True, check=True)

        # Increase sending buffer size.
        subprocess.run('/sbin/ifconfig ' + self.interface + ' txqueuelen 1000', shell=True, check=True)

    def send(self, data):
        msg = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.sending_bus.send(msg)
            print('Message sent on {}.'.format(self.sending_bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

        time.sleep(self.delay)

    def receive(self):
        try:
            msg = self.receiving_bus.recv(0.0) # Non-blocking read.

            if msg is not None:
                print('Message received on {}.'.format(self.receiving_bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

        return msg

    def condition_met(self):
        msg = self.receive()
        if msg is not None: # Message seen on CAN bus.
            if msg.arbitration_id == 1: # SYNC received from control bridge.
                time.sleep(self.time_base * (self.arbitration_id - 1)) # Wait for own turn.
                return (msg[0] & 0x10) == 0x10 # TSO CAN protocol code for pick up object command.
        return False

