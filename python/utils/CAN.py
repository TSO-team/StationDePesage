#!/usr/bin/env python3

# File:        utils/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: TSO protocol for CAN bus.

from __future__ import print_function
import can, os, signal, subprocess, time

class Protocol:
    def __init__(self, interface_type='vcan', arbitration_id=3, bitrate=50000, time_base=0.02):
        self.arbitration_id = arbitration_id
        self.interface_type = interface_type
        self.time_base = time_base

        constructor_arguments = self.pre_configure_CAN(channel='socketcan', bitrate=bitrate, is_extended_id=False)

        self.sending_bus = can.interface.Bus(**constructor_arguments)
        self.receiving_bus = can.interface.Bus(**constructor_arguments)

        self.handle_exit_signals()

    def reset(self):
        subprocess.run('/home/debian/workspace/StationDePesage/utils/CAN/epilog.sh %s' % self.interface, shell=True, check=True)
        print('CAN closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

    def pre_configure_CAN(self, channel='socketcan', bitrate=50000, is_extended_id=False):
        self.interface = self.interface_type + str(0)
        self.channel = channel
        self.bitrate = bitrate
        self.is_extended_id = is_extended_id

        constructor_arguments = {'channel': self.channel}

        # Virtual CAN interface has no bitrate.
        if self.interface_type != 'vcan':
            constructor_arguments['bitrate'] = self.bitrate
            self.bustype = self.interface
        else:
            self.bustype = 'virtual'

        prelude = '/home/debian/workspace/StationDePesage/utils/CAN/prelude.sh %s %d %d %.2f'
        prelude %= (self.interface, self.arbitration_id, self.bitrate, self.time_base)
        subprocess.run(prelude, shell=True, check=True)

        constructor_arguments['bustype'] = self.bustype

        return constructor_arguments

    def send(self, data):
        msg = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.sending_bus.send(msg)
            print('Message sent on {}.'.format(self.sending_bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

    def receive(self):
        try:
            msg = self.receiving_bus.recv(0.0) # Non-blocking read.

            if msg is not None:
                print('Message received on {}.'.format(self.receiving_bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

        return msg

    def condition_met(self):
        if self.interface_type == 'vcan':
            return True
        else:
            msg = self.receive()
            if msg is not None: # Message seen on CAN bus.
                if msg.arbitration_id == 1: # SYNC received from control bridge.
                    time.sleep(self.time_base * (self.arbitration_id - 1)) # Wait for own turn.
                    return (msg.data[0] & 0x10) == 0x10 # TSO CAN protocol code for pick up object command.
            return False

