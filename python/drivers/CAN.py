#!/usr/bin/env python3

# File:        python/drivers/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: Driver for CAN bus.

from __future__ import print_function
import can

class CAN_driver:
    def CAN_init_driver(self, interface_type='vcan', bitrate=50000):
        self.CAN_initialize_default_arguments(channel='socketcan', is_extended_id=False)
        self.CAN_initialize_configurable_arguments(interface_type=interface_type, bitrate=bitrate)
        constructor_arguments = self.CAN_initialize_inferred_arguments()

        self.sending_bus = can.interface.Bus(**constructor_arguments)
        self.receiving_bus = can.interface.Bus(**constructor_arguments)

    def CAN_initialize_default_arguments(self, channel='socketcan', is_extended_id=False):
        self.channel = channel
        self.is_extended_id = is_extended_id

    def CAN_initialize_configurable_arguments(self, interface_type='vcan', bitrate=50000):
        self.interface_type = interface_type
        self.bitrate = bitrate

    def CAN_initialize_inferred_arguments(self):
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

    def CAN_send(self, arbitration_id, data):
        CAN_message_send = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.sending_bus.send(CAN_message_send)
            print('Message sent on {}.'.format(self.sending_bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

    def CAN_receive(self):
        try:
            CAN_message_received = self.receiving_bus.recv(0.0) # Non-blocking read.

            if CAN_message_received is not None:
                print('Message received on {}.'.format(self.receiving_bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

        return CAN_message_received

