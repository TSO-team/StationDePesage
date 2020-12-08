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
from utils.payload import add_payload_args
from utils.CAN import add_CAN_args
import argparse, datetime, os, shlex, signal, subprocess, sys, time

def parse_args():
    parser = argparse.ArgumentParser(description='Test uARM for object detection using I2C VL6180X Time-of-Flight sensor to scan until object is found.', 
                                     formatter_class=argparse.RawTextHelpFormatter)
    add_payload_args(parser)
    add_CAN_args(parser)
    return parser.parse_args()

'''
def spawn_process_and_get_pid():
    command = '/usr/bin/nohup /usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM_payload.py & /bin/echo $$ > /tmp/weight'
    os.system(command)
    with open('/tmp/weight', 'r') as f:
         pid = f.readline()[:-1]
    return pid
'''

def get_child_weight():
    path = Path('/tmp/weight')
    if path.stat().st_size == 0:
        weight = None
    else:
        f = open(path, 'r')
        weight = f.readline()[:-1]
        f.close()
    return weight

def spawn_process_and_get_pid(args):
    args = vars(args)
    args = shlex.split(args)
    command_0 = '/usr/bin/nohup'
    command_1 = '/usr/bin/python3'
    command_2 = '/home/debian/workspace/StationDePesage/python/uARM_payload.py'
    command_fork = '& /bin/echo $$ > /tmp/weight'
    proc = subprocess.Popen([command_0, command_1, command_2, args, command_fork], shell=True)
    time.sleep(3)
    pid = get_child_weight()
    return proc, pid

def main():
    args = parse_args()
    printable_args = vars(args)
    print(printable_args)

    printable_args = shlex.split(printable_args)
    is_factory_reset = False

    TSO_protocol = CAN.Protocol(interface_type=args.can_interface_type, arbitration_id=args.can_id, bitrate=args.can_bitrate, time_base=args.can_time_base)
    CAN_message_received = None
    time_base_in_microseconds = float(TSO_protocol.time_base) * 10000000.0

    proc, pid = spawn_process_and_get_pid(args)

    while True:
        CAN_message_received_old = CAN_message_received.copy()
        CAN_message_received = TSO_protocol.receive()

        if is_factory_reset:
            if CAN_message_received is not None: # Message seen on CAN bus.
                if TSO_protocol.is_error(CAN_message_received):
                    CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                else:
                    proc, pid = spawn_process_and_get_pid(args)
                    is_factory_reset = False
                    break
        else:
            timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
            timestamp += datetime.timedelta(milliseconds=int(time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))

            while True:
                if CAN_message_received is not None: # Message seen on CAN bus.
                    if TSO_protocol.is_error(CAN_message_received):
                        CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                        is_factory_reset = True
                        break
                    if CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                        unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
                        if unit is not None:
                            os.kill(pid, signal.SIGUSR1) # Request weights.
                timestamp_parsed = int(timestamp.microsecond / time_base_in_microseconds)
                timestamp_now = datetime.datetime.fromtimestamp(time.time())
                timestamp_now_parsed = int(timestamp_now.microsecond / time_base_in_microseconds)
                if timestamp_parsed > timestamp_now_parsed:
                    CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_TIMESTAMP)
                    is_factory_reset = True
                    break
                elif timestamp_parsed == timestamp_now_parsed:
                    break
                else:
                    weight = get_child_weight()
                    if weight is not None:
                        CAN_message_send.data[1] = weight
                        CAN_message_send.data[0] &= 0xFE
                        CAN_message_send.data[0] |= unit

        TSO_protocol.send(CAN_message_send)

        if is_factory_reset:
            proc.terminate()

if __name__ == '__main__':
    main()

