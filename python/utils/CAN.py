#!/usr/bin/env python3

# File:        python/utils/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: TSO protocol for CAN bus.

from __future__ import print_function
import can, os, signal, subprocess, time

class Protocol:
    def __init__(self, interface_type='vcan', arbitration_id=3, bitrate=50000, time_base=0.02):
        self.initialize_default_arguments(channel='socketcan', is_extended_id=False)
        self.initialize_configurable_arguments(interface_type=interface_type, arbitration_id=arbitration_id, bitrate=bitrate, time_base=time_base)
        constructor_arguments = self.initialize_inferred_arguments()

        self.pre_configure_CAN()

        self.sending_bus = can.interface.Bus(**constructor_arguments)
        self.receiving_bus = can.interface.Bus(**constructor_arguments)

        self.set_CAN_protocol()
        self.handle_exit_signals()

    def reset(self):
        subprocess.run('/home/debian/workspace/StationDePesage/utils/CAN/epilog.sh %s &' % self.interface)
        print('CAN closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.

    def initialize_default_arguments(self, channel='socketcan', is_extended_id=False):
        self.channel = channel
        self.is_extended_id = is_extended_id

    def initialize_configurable_arguments(self, interface_type='vcan', arbitration_id=3, bitrate=50000, time_base=0.02):
        self.interface_type = interface_type
        self.arbitration_id = arbitration_id
        self.bitrate = bitrate
        self.time_base = time_base

    def initialize_inferred_arguments(self):
        self.interface = self.interface_type + str(0)

        constructor_arguments = {'channel': self.channel}

        # Virtual CAN interface has no bitrate.
        if self.interface_type != 'vcan':
            constructor_arguments['bitrate'] = self.bitrate
            self.bustype = self.interface
        else:
            self.bustype = 'virtual'

        constructor_arguments['bustype'] = self.bustype

        return constructor_arguments

    def pre_configure_CAN(self):
        prelude = '/home/debian/workspace/StationDePesage/utils/CAN/prelude.sh %s %d %d %.2f'
        subprocess.run(prelude % (self.interface, self.arbitration_id, self.bitrate, self.time_base))

    def set_CAN_protocol(self):
        self.ERROR_UNSPECIFIED = 0x80
        self.ERROR_PROTOCOL = 0xA0
        self.ERROR_TIMEOUT = 0xC0
        self.ERROR_RETRANSMIT = 0xE0

    def is_error(self, CAN_message):
        return CAN_message.data[0] > 127

    def set_error_message(self, CAN_message, error_code=None):
        if error_code is None:
            error_code = self.ERROR_UNSPECIFIED
        else:
            error_code &= 0xE0

        CAN_message.data[0] &= 0x1F
        CAN_message.data[0] |= error_code

        return CAN_message

    def payload_received(self, CAN_message_received, CAN_message_received_old):
        pass

    def parse_balance_output(self, weight, unit):
        pass

    def send(self, data):
        CAN_message_send = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.sending_bus.send(CAN_message_send)
            print('Message sent on {}.'.format(self.sending_bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

    def receive(self):
        try:
            CAN_message_received = self.receiving_bus.recv(0.0) # Non-blocking read.

            if CAN_message_received is not None:
                print('Message received on {}.'.format(self.receiving_bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

        return CAN_message_received

    def condition_met(self): # Test mode.
        if self.interface_type == 'vcan':
            return True
        else:
            CAN_message_received = self.receive()
            if CAN_message_received is not None: # Message seen on CAN bus.
                if CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                    time.sleep(self.time_base * (self.arbitration_id - 1)) # Wait for own turn.
                    return (CAN_message_received.data[0] & 0x18) == 0x08 # TSO CAN protocol code for pick up object command.
            return False

