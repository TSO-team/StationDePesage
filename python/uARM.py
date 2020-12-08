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
    parser = argparse.ArgumentParser(description='Run parent process main control loop using child process for calling '
                                                 'balance/buzzer/sensor/uARM payload through SIGUSR1 and retrieving balance '
                                                 'weights using popen communication feedback.', 
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
'''

'''
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
'''

def spawn_process_and_get_pid(args):
    args = shlex.split(vars(args))
    python_command = '/usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM_payload.py'
    proc = subprocess.Popen([python_command, args], shell=True)
    time.sleep(3)
    return proc, proc.pid

def generate_timestamp_and_parsed_timestamp(time_base_in_microseconds, TSO_protocol=None):
    timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    if TSO_protocol is not None:
        timestamp += datetime.timedelta(milliseconds=int(time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))
    timestamp_parsed = int(timestamp.microsecond / time_base_in_microseconds)
    return timestamp, timestamp_parsed

def prepare_weight_for_CAN_transmit_if_received_from_child(proc, CAN_message_send, unit):
    weight = proc.communicate()
    if weight is not None:
        CAN_message_send.data[1] = weight
        CAN_message_send.data[0] &= 0xFE
        CAN_message_send.data[0] |= unit
    return CAN_message_send

def request_weight_from_child_if_CAN_wants_it(TSO_protocol, CAN_message_received, CAN_message_received_old):
    unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
    if unit is not None:
        os.kill(pid, signal.SIGUSR1) # Request weights from child.
    return unit

def main():
    args = parse_args()
    print(vars(args))

    TSO_protocol = CAN.Protocol(interface_type=args.can_interface_type, arbitration_id=args.can_id, bitrate=args.can_bitrate, time_base=args.can_time_base)
    time_base_in_microseconds = float(TSO_protocol.time_base) * 10000000.0
    CAN_message_received = None
    is_factory_reset = False

    proc, pid = spawn_process_and_get_pid(args)
    timestamp, timestamp_parsed = generate_timestamp_and_parsed_timestamp(time_base_in_microseconds, TSO_protocol=TSO_protocol)

    while True:
        CAN_message_received_old = CAN_message_received.copy()
        CAN_message_received = TSO_protocol.receive()

        if is_factory_reset:
            if CAN_message_received is not None: # Message seen on CAN bus.
                if TSO_protocol.is_error(CAN_message_received):
                    CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                else:
                    proc, pid = spawn_process_and_get_pid(args)
                    timestamp, timestamp_parsed = generate_timestamp_and_parsed_timestamp(time_base_in_microseconds, TSO_protocol=TSO_protocol)
                    is_factory_reset = False
                    break
        else:
            if CAN_message_received is not None: # Message seen on CAN bus.
                if TSO_protocol.is_error(CAN_message_received):
                    CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                    is_factory_reset = True
                elif CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                    timestamp, timestamp_parsed = generate_timestamp_and_parsed_timestamp(time_base_in_microseconds, TSO_protocol=TSO_protocol)
                    unit = request_weight_from_child_if_CAN_wants_it(TSO_protocol, CAN_message_received, CAN_message_received_old)

            timestamp_now, timestamp_now_parsed = generate_timestamp_and_parsed_timestamp(time_base_in_microseconds)

            if timestamp_parsed > timestamp_now_parsed:
                CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_TIMESTAMP)
                is_factory_reset = True
            elif timestamp_parsed < timestamp_now_parsed:
                CAN_message_send = prepare_weight_for_CAN_transmit_if_received_from_child(proc, CAN_message_send, unit)

        TSO_protocol.send(CAN_message_send)

        if is_factory_reset:
            proc.terminate()

if __name__ == '__main__':
    main()

