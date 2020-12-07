#!/usr/bin/env python3

# File:        python/uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        - implement missing functionality:
#                  - merge fork with separated, monolithic payload:
#                      - Ensure C follows Python closely and vice-versa
#                - grab weight from child through TTY.
#                  - balance to CAN (balance currently sends its output to TTY which is grabbed but not parsed)
#              - translate to C (see C)
#              - trap SIGUSR1 and others as child
# For help:      python3 python/uARM_payload.py --help # <-- Use --help for help using this file like this. <--

from __future__ import print_function
from utils import CAN
import datetime, os, signal, sys, time

def parse_args():
    parser = argparse.ArgumentParser(description='Test uARM for object detection using I2C VL6180X Time-of-Flight sensor to scan until object is found.')
    parser.add_argument('--first-x-position', metavar='<first-x-position>', type=float, required=False, default=21.6, help='First position on X axis.')
    parser.add_argument('--first-y-position', metavar='<first-y-position>', type=float, required=False, default=80.79, help='First position on Y axis.')
    parser.add_argument('--first-z-position', metavar='<first-z-position>', type=float, required=False, default=186.11, help='First position on Z axis.')
    parser.add_argument('--second-x-position', metavar='<second-x-position>', type=float, required=False, default=-232.97, help='Second absolute position to X axis.')
    parser.add_argument('--second-y-position', metavar='<second-y-position>', type=float, required=False, default=120.86, help='Second absolute position to Y axis.')
    parser.add_argument('--second-z-position', metavar='<second-z-position>', type=float, required=False, default=126.59, help='Second absolute position to Z axis.')
    parser.add_argument('--third-x-position', metavar='<third-x-position>', type=float, required=False, default=313.93, help='Third absolute position to X axis.')
    parser.add_argument('--third-y-position', metavar='<third-y-position>', type=float, required=False, default=18.76, help='Third absolute position to Y axis.')
    parser.add_argument('--third-z-position', metavar='<third-z-position>', type=float, required=False, default=178.67, help='Third absolute position to Z axis.')
    parser.add_argument('--scan-x-displacement', metavar='<scan-x-displacement>', type=float, required=False, default=5.0, help='Relative position X axis displacement for scans.')
    parser.add_argument('--scan-y-displacement', metavar='<scan-y-displacement>', type=float, required=False, default=5.0, help='Relative position Y axis displacement for scans.')
    parser.add_argument('--scan-z-displacement', metavar='<scan-z-displacement>', type=float, required=False, default=0.0, help='Relative position Z axis displacement for scans.')
    parser.add_argument('--stride-x', metavar='<stride-x>', type=int, required=False, default=2, help='One step on X axis.')
    parser.add_argument('--stride-y', metavar='<stride-y>', type=int, required=False, default=2, help='One step on Y axis.')
    parser.add_argument('--stride-z', metavar='<stride-z>', type=int, required=False, default=0, help='One step on Z axis.')
    parser.add_argument('--speed', metavar='<speed>', type=int, required=False, default=150, help='Speed of uARM displacements.')
    parser.add_argument('--uarm-tty-port', metavar='<uarm-tty-port>', type=str, required=False, default='/dev/ttyUSB1', help='uARM UART TTY port.')
    parser.add_argument('--balance-tty-port', metavar='<balance-tty-port>', type=str, required=False, default='/dev/ttyUSB0', help='Balance UART TTY port.')
    parser.add_argument('--sensor-i2c-port', metavar='<sensor-i2c-port>', type=int, required=False, default=1, help='I2C port for Time-of-Flight (VL6180X) sensor.')
    parser.add_argument('--sensor-threshold', metavar='<sensor-threshold>', type=float, required=False, default=0.5, help='VL6180X sensor threshold for object detection.')
    parser.add_argument('--buzzer-frequency-multiplier', metavar='<buzzer-frequency-multiplier>', type=float, required=False, default=1.0, help='Buzzer frequency multiplier.')
    parser.add_argument('--buzzer-duration-multiplier', metavar='<buzzer-duration-multiplier>', type=float, required=False, default=3.0, help='Buzzer duration multiplier.')
    parser.add_argument('--uart-delay', metavar='<uart-delay>', type=float, required=False, default=2.0, help='Delay after configuring uARM\'s UART port.')
    parser.add_argument('--grab-delay', metavar='<grab-delay>', type=float, required=False, default=5.0, help='Delay after uARM grabs object.')
    parser.add_argument('--drop-delay', metavar='<drop-delay>', type=float, required=False, default=5.0, help='Delay after uARM drops object.')
    parser.add_argument('--pump-delay', metavar='<pump-delay>', type=float, required=False, default=5.0, help='Delay after uARM (de-)pumps object.')
    parser.add_argument('--servo-attach-delay', metavar='<servo-attach-delay>', type=float, required=False, default=5.0, help='Delay after uARM attaches servos.')
    parser.add_argument('--servo-detach-delay', metavar='<servo-detach-delay>', type=float, required=False, default=5.0, help='Delay after uARM detaches servos.')
    parser.add_argument('--set-position-delay', metavar='<set-position-delay>', type=float, required=False, default=5.0, help='Delay after uARM set to position.')
    parser.add_argument('--transition-delay', metavar='<transition-delay>', type=float, required=False, default=5.0, help='Delay after using uARM buzzer signals the end of a phase and allows world to react.')
    parser.add_argument('--can-interface-type', metavar='<can-interface-type>', type=str, required=False, default='vcan', help='One of \'vcan\' or \'can\'.')
    parser.add_argument('--can-id', metavar='<can-id>', type=int, required=False, default=3, help='The number of the station on the CAN network.')
    parser.add_argument('--can-bitrate', metavar='<can-bitrate>', type=int, required=False, default=50000, help='Bitrate on CAN network.')
    parser.add_argument('--can-time-base', metavar='<can-time-base>', type=float, required=False, default=0.02, help='Time base in seconds regulating the time lapse when each station can transmit in turn on the CAN network.')
    parser.add_argument('--can-delay', metavar='<can-delay>', type=float, required=False, default=2.0, help='CAN delay.')
    return parser.parse_args()

def main():
    import argparse
    args = parse_args()
    print(vars(args))

    r, w = os.pipe()

    ppid = os.getpid()
    return_value = os.fork()
    pid = os.getpid()

    if return_value is 0: # child
        os.close(r)
        w = os.fdopen(w, 'w')
        #os.execl('/usr/bin/python3', '/home/debian/workspace/StationDePesage/python/uARM_payload.py')
        #sys.exit(1)
        w.write('This message sent from child to parent is a test.')
        w.close()
        sys.exit(0)
    else: # parent
        os.close(w)
        r = os.fdopen(r)
        string = r.read()
        print('Parent received message:', string)

        TSO_protocol = CAN.Protocol(interface_type=args.interface_type, arbitration_id=args.can_id, bitrate=args.can_bitrate, time_base=args.can_time_base)
        CAN_message_received = None
        time_base_in_microseconds = float(TSO_protocol.time_base) * 10000000.0

        '''
        while True:
            CAN_message_received_old = CAN_message_received.copy()
            CAN_message_received = TSO_protocol.receive()

            timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
            timestamp += datetime.timedelta(milliseconds=int(time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))

            while True:
                if CAN_message_received is not None: # Message seen on CAN bus.
                    if TSO_protocol.is_error(CAN_message_received):
                        CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                        os.kill(pid, signal.SIGINT)
                        break
                    if CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                        unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
                        if unit is not None:
                            os.kill(pid, signal.SIGUSR1) # Run uARM payload.
                timestamp_parsed = int(timestamp.microsecond / time_base_in_microseconds)
                timestamp_now = datetime.datetime.fromtimestamp(time.time())
                timestamp_now_parsed = int(timestamp_now.microsecond / time_base_in_microseconds)
                if timestamp_parsed > timestamp_now_parsed:
                    CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_TIMESTAMP)
                    os.kill(pid, signal.SIGINT)
                    break
                elif timestamp_parsed == timestamp_now_parsed:
                    break
                else:
                    continue

            TSO_protocol.send(CAN_message_send)
        '''

        sys.exit(0)

if __name__ == '__main__':
    main()

