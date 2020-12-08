#!/usr/bin/env python3

# File:        python/utils/CAN.py
# By:          Samuel Duclos
# For:         My team.
# Description: TSO protocol for CAN bus.

from __future__ import print_function
import can, os, signal, subprocess, time

def add_CAN_args(parser):
    parser.add_argument('--can-interface-type', metavar='<can-interface-type>', type=str, required=False, default='vcan', help='One of \'vcan\' or \'can\'.')
    parser.add_argument('--can-id', metavar='<can-id>', type=int, required=False, default=3, help='The number of the station on the CAN network.')
    parser.add_argument('--can-bitrate', metavar='<can-bitrate>', type=int, required=False, default=50000, help='Bitrate on CAN network.')
    parser.add_argument('--can-time-base', metavar='<can-time-base>', type=float, required=False, default=0.02, help='Time base in seconds regulating the time lapse when each station can transmit in turn on the CAN network.')
    parser.add_argument('--can-delay', metavar='<can-delay>', type=float, required=False, default=2.0, help='CAN delay.')
    return parser.parse_args()

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
        epilog = '/bin/bash /home/debian/workspace/StationDePesage/bash/CAN/epilog.sh %s'
        os.system(epilog % self.interface_type)
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
        self.CAN_message_received_old = None
        self.CAN_message_received = None
        self.CAN_message_send = None

    def initialize_configurable_arguments(self, interface_type='vcan', arbitration_id=3, bitrate=50000, time_base=0.02):
        self.interface_type = interface_type
        self.arbitration_id = arbitration_id
        self.bitrate = bitrate
        self.time_base = time_base

    def initialize_inferred_arguments(self):
        self.time_base_in_microseconds = float(self.time_base) * 10000000.0
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
        prelude = '/bin/bash /home/debian/workspace/StationDePesage/bash/CAN/prelude.sh %s %d %d %.2f'
        os.system(prelude % (self.interface_type, self.arbitration_id, self.bitrate, self.time_base))

    def set_CAN_protocol(self):
        self.OFF = 0x00
        self.ON = 0x20
        self.WAIT = 0x40
        self.TEST = 0x60
        self.ERROR_UNSPECIFIED = 0x80
        self.ERROR_PROTOCOL = 0xA0
        self.ERROR_TIMEOUT = 0xC0
        self.ERROR_RETRANSMIT = 0xE0
        self.NOTHING = 0x00
        self.BLACK = 0x08
        self.ORANGE = 0x10
        self.OTHER = 0x18
        self.A = 0x00
        self.B = 0x02
        self.C = 0x04
        self.D = 0x06
        self.GRAMS = 0x00
        self.OZ = 0x01

    def is_error(self, CAN_message):
        return CAN_message.data[0] > 127

    def set_error_message(self, CAN_message_send, error_code=None):
        self.CAN_message_send = CAN_message_send

        if error_code is None:
            error_code = self.ERROR_UNSPECIFIED
        else:
            error_code &= 0xE0

        self.CAN_message_send.data[0] &= 0x1F
        self.CAN_message_send.data[0] |= error_code

    def get_mode(self, CAN_message_received):
        return CAN_message_received.data[0] & 0xE0

    def get_unit(self, CAN_message_received):
        return CAN_message_received.data[0] & 0x01

    def get_color(self, CAN_message_received):
        return CAN_message_received_old.data[0] & 0x18

    def atoi(self, a):
        return int(a.strip())

    def payload_received(self, CAN_message_received, CAN_message_received_old):
        old_mode = self.get_mode(CAN_message_received_old)
        mode = self.get_mode(CAN_message_received)

        old_color = self.get_color(CAN_message_received_old)
        color = self.get_color(CAN_message_received)

        unit = self.get_unit(CAN_message_received)

        if old_mode != mode and old_color != color and mode == self.ON and color == self.BLACK:
            return unit
        else:
            return None

    def parse_balance_output(self, weight, unit):
        pass

    def prepare_CAN_message_for_weight_transmission(self, CAN_message_send, weight):
        if weight is not None:
            CAN_message_send.data[1] = weight
            CAN_message_send.data[0] &= 0xFE
            CAN_message_send.data[0] |= unit
        return CAN_message_send

    def send(self, data):
        self.CAN_message_send = can.Message(arbitration_id=self.arbitration_id, data=data, is_extended_id=self.is_extended_id)

        try:
            self.sending_bus.send(self.CAN_message_send)
            print('Message sent on {}.'.format(self.sending_bus.channel_info))
        except can.CanError:
            print('CAN ERROR WHILE SENDING MESSAGE!')

    def receive(self):
        try:
            self.CAN_message_received_old = self.CAN_message_received.copy()
            self.CAN_message_received = self.receiving_bus.recv(0.0) # Non-blocking read.

            if self.CAN_message_received is not None:
                print('Message received on {}.'.format(self.receiving_bus.channel_info))

        except can.CanError:
            print('CAN ERROR WHILE RECEIVING MESSAGE!')

    def condition_met(self): # Test mode.
        if self.interface_type == 'vcan':
            return True
        else:
            self.receive()
            if self.CAN_message_received is not None: # Message seen on CAN bus.
                if self.CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                    time.sleep(self.time_base * (self.arbitration_id - 1)) # Wait for own turn.
                    return (self.CAN_message_received.data[0] & 0x18) == 0x08 # TSO CAN protocol code for pick up object command.
            return False

