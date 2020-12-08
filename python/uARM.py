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

def spawn_process_and_get_pid(args):
    args = shlex.split(vars(args))
    python_command = '/usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM_payload.py'
    proc = subprocess.Popen([python_command, args], shell=True)
    time.sleep(3)
    return proc, proc.pid

def generate_timestamp(TSO_protocol):
    timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    read_timeout = timestamp + datetime.timedelta(milliseconds=int(TSO_protocol.time_base_in_microseconds) * TSO_protocol.number_of_stations)
    write_timeout = timestamp + datetime.timedelta(milliseconds=int(TSO_protocol.time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))
    timestamp = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    read_timeout = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    write_timeout = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    return timestamp, read_timeout, write_timeout

def request_weight_from_child_if_CAN_wants_it(TSO_protocol, CAN_message_received, CAN_message_received_old):
    unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
    if unit is not None:
        os.kill(pid, signal.SIGUSR1) # Request weights from child.
    return unit

def main():
    args = parse_args()
    print(vars(args))

    TSO_protocol = CAN.Protocol(interface_type=args.can_interface_type, 
                                arbitration_id=args.can_id, 
                                bitrate=args.can_bitrate, 
                                time_base=args.can_time_base, 
                                number_of_stations=args.can_number_of_stations)

    proc, pid = spawn_process_and_get_pid(args)
    timestamp, read_timeout, write_timeout = generate_timestamp(TSO_protocol)
    is_factory_reset = False

    while True:
        TSO_protocol.receive()

        if TSO_protocol.CAN_message_received is not None: # Message seen on CAN bus.
            if TSO_protocol.is_error():
                TSO_protocol.set_error_message(error_code=TSO_protocol.ERROR_RETRANSMIT)
                is_factory_reset = True
            elif is_factory_reset:
                proc, pid = spawn_process_and_get_pid(args)
                timestamp, read_timeout, write_timeout = generate_timestamp(TSO_protocol)
                is_factory_reset = False
            elif TSO_protocol.CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                timestamp, read_timeout, write_timeout = generate_timestamp(TSO_protocol)
                unit = request_weight_from_child_if_CAN_wants_it(TSO_protocol, TSO_protocol.CAN_message_received, TSO_protocol.CAN_message_received_old)

            timestamp_now, _, _ = generate_timestamp(TSO_protocol)

            if timestamp_now > read_timeout:
                TSO_protocol.set_error_message(error_code=TSO_protocol.ERROR_TIMESTAMP)
                is_factory_reset = True
            elif timestamp_now > write_timeout:
                TSO_protocol.send(TSO_protocol.CAN_message_send)
            else:
                weight = proc.communicate()
                TSO_protocol.CAN_message_send = TSO_protocol.prepare_CAN_message_for_weight_transmission(weight, unit)

        if is_factory_reset:
            proc.terminate()

if __name__ == '__main__':
    main()

