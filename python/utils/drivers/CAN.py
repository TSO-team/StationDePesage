#!/usr/bin/env python3

# File:        python/utils/drivers/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: Driver for CAN bus.

from __future__ import print_function
import can

class CAN_driver:
<<<<<<< HEAD:python/utils/drivers/CAN.py
    def __init__(self, channel='vcan0', interface_type='socketcan', bitrate=50000):
        self.CAN_init_driver(channel=channel, interface_type=interface_type, bitrate=bitrate)

    def CAN_init_driver(self, channel='vcan0', interface_type='virtual', bitrate=50000):
        self.is_extended_id = False
        self.CAN_initialize_configurable_arguments(channel=channel, interface_type=interface_type, bitrate=bitrate)
=======
    def __init__(self, interface_type='vcan', bitrate=50000):
        self.CAN_init_driver(interface_type=interface_type, bitrate=bitrate)

    def CAN_init_driver(self, interface_type='vcan', bitrate=50000):
        self.CAN_initialize_default_arguments(channel='socketcan', is_extended_id=False)
        self.CAN_initialize_configurable_arguments(interface_type=interface_type, bitrate=bitrate)
>>>>>>> 0ccfa61942c6796f7da346360fba7a4fa3cec44e:python/utils/drivers/CAN.py
        constructor_arguments = self.CAN_initialize_inferred_arguments()

        print(constructor_arguments)

        self.sending_bus = can.interface.Bus(**constructor_arguments)
        self.receiving_bus = can.interface.Bus(**constructor_arguments)

        #self.handle_exit_signals()
<<<<<<< HEAD:python/utils/drivers/CAN.py
=======

    def CAN_initialize_default_arguments(self, channel='socketcan', is_extended_id=False):
        self.channel = channel
        self.is_extended_id = is_extended_id
>>>>>>> 0ccfa61942c6796f7da346360fba7a4fa3cec44e:python/utils/drivers/CAN.py

    def CAN_initialize_configurable_arguments(self, channel='can0', interface_type='socketcan', bitrate=50000):
        self.channel = channel
        self.interface_type = interface_type
        self.bitrate = bitrate

    def CAN_initialize_inferred_arguments(self):
        self.interface = self.interface_type + str(0)

        constructor_arguments = {'channel': self.channel}

        # Virtual CAN interface has no bitrate.
        if self.interface_type != 'vcan':
            constructor_arguments['bitrate'] = self.bitrate
            self.bustype = self.interface_type
            constructor_arguments['bustype'] = 'socketcan'
        else:
            constructor_arguments['bustype'] = 'virtual'

        self.bustype = constructor_arguments['bustype']
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

    '''
    def reset(self):
        print('CAN closed...')

    def __del__(self):
        self.reset()

    def handle_exit_signals(self):
        signal.signal(signal.SIGINT, self.reset) # Handles CTRL-C for clean up.
        signal.signal(signal.SIGHUP, self.reset) # Handles stalled process for clean up.
        signal.signal(signal.SIGTERM, self.reset) # Handles clean exits for clean up.
    '''

