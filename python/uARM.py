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

def generate_timestamp_and_parsed_timestamp(time_base_in_microseconds, TSO_protocol=None):
    timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    if TSO_protocol is not None:
        timestamp += datetime.timedelta(milliseconds=int(time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))
    timestamp_parsed = int(timestamp.microsecond / time_base_in_microseconds)
    return timestamp, timestamp_parsed

def generate_timestamp_and_parsed_timestamp(TSO_protocol):
    timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    timestamp_read_timeout = timestamp + datetime.timedelta(milliseconds=int(TSO_protocol.time_base_in_microseconds) * TSO_protocol.number_of_stations)
    timestamp_write_timeout = timestamp + datetime.timedelta(milliseconds=int(TSO_protocol.time_base_in_microseconds) * (TSO_protocol.arbitration_id - 1))
    timestamp_parsed = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    timestamp_read_timeout_parsed = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    timestamp_write_timeout_parsed = int(timestamp.microsecond / TSO_protocol.time_base_in_microseconds)
    return timestamp, timestamp_parsed, timestamp_read_timeout, timestamp_read_timeout_parsed, timestamp_write_timeout, timestamp_write_timeout_parsed

def request_weight_from_child_if_CAN_wants_it(TSO_protocol, CAN_message_received, CAN_message_received_old):
    unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
    if unit is not None:
        os.kill(pid, signal.SIGUSR1) # Request weights from child.
    return unit

def main():
    args = parse_args()
    print(vars(args))

    TSO_protocol = CAN.Protocol(interface_type=args.can_interface_type, arbitration_id=args.can_id, bitrate=args.can_bitrate, time_base=args.can_time_base, number_of_stations=args.can_number_of_stations)
    is_factory_reset = False

    proc, pid = spawn_process_and_get_pid(args)
    timestamp, timestamp_parsed, timestamp_read_timeout, timestamp_write_timeout = generate_timestamp_and_parsed_timestamp(TSO_protocol)

    while True:
        TSO_protocol.receive()

        if CAN_message_received is not None: # Message seen on CAN bus.
            if TSO_protocol.is_error(TSO_protocol.CAN_message_received):
                TSO_protocol.set_error_message(TSO_protocol.CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                is_factory_reset = True
            elif is_factory_reset:
                proc, pid = spawn_process_and_get_pid(args)
                timestamp, timestamp_parsed, timestamp_read_timeout, timestamp_read_timeout_parsed, timestamp_write_timeout, timestamp_write_timeout_parsed = generate_timestamp_and_parsed_timestamp(TSO_protocol)
                is_factory_reset = False
            elif TSO_protocol.CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                timestamp, timestamp_parsed, timestamp_read_timeout, timestamp_read_timeout_parsed, timestamp_write_timeout, timestamp_write_timeout_parsed = generate_timestamp_and_parsed_timestamp(TSO_protocol)
                unit = request_weight_from_child_if_CAN_wants_it(TSO_protocol, TSO_protocol.CAN_message_received, TSO_protocol.CAN_message_received_old)

            timestamp_now, timestamp_now_parsed, timestamp_now_read_timeout, timestamp_now_read_timeout_parsed, timestamp_now_write_timeout, timestamp_now_write_timeout_parsed = generate_timestamp_and_parsed_timestamp(TSO_protocol)

            if timestamp_now_parsed > timestamp_read_timeout_parsed:
                TSO_protocol.set_error_message(TSO_protocol.CAN_message_received, error_code=TSO_protocol.ERROR_TIMESTAMP)
                is_factory_reset = True
            elif timestamp_now_parsed > timestamp_write_timeout_parsed:
                TSO_protocol.send(TSO_protocol.CAN_message_send.data)
            else timestamp_parsed < timestamp_now_parsed:
                weight = proc.communicate()
                TSO_protocol.CAN_message_send = TSO_protocol.prepare_CAN_message_for_weight_transmission(TSO_protocol.CAN_message_send, weight)

        if is_factory_reset:
            proc.terminate()

if __name__ == '__main__':
    main()

