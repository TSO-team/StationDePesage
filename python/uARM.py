#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:        - parallelize processes
#              - implement missing functionality
#              - translate to C

from __future__ import print_function
from utils import balance, buzzer, CAN, sensor, uarm
import datetime, multiprocessing, os, time

CAN_interface_type, CAN_ID, CAN_bitrate, CAN_time_base = 'vcan', 3, 50000, 0.02 # 20 milliseconds between each station.
uarm_tty_port, balance_tty_port = '/dev/ttyUSB1', '/dev/ttyUSB0'
sensor_i2c_port, sensor_threshold = 1, 0.5
buzzer_frequency_multiplier, buzzer_duration_multiplier = 1.0, 3.0
uart_delay, grab_delay, drop_delay, pump_delay, CAN_delay = 2, 5, 5, 5, 2 # seconds
servo_attach_delay, set_position_delay, servo_detach_delay, transition_delay = 5, 5, 5, 5 # seconds

initial_position = {'x': 21.6, 'y': 80.79, 'z': 186.11, 'speed': 150, 'relative': False, 'wait': True}
balance_position = {'x': 313.93, 'y': 18.76, 'z': 178.67, 'speed': 150, 'relative': False, 'wait': True}
vehicle_position = {'x': -232.97, 'y': 120.86, 'z': 126.59, 'speed': 150, 'relative': False, 'wait': True}

uarm = uarm.UARM(uarm_tty_port='/dev/ttyUSB1', 
                 uart_delay=uart_delay, 
                 initial_position=initial_position, 
                 servo_attach_delay=servo_attach_delay, 
                 set_position_delay=set_position_delay, 
                 servo_detach_delay=servo_detach_delay, 
                 pump_delay=pump_delay)

buzzer = buzzer.Buzzer(uarm=uarm.uarm, servo_detach_delay=uarm.servo_detach_delay, transition_delay=transition_delay)
sensor = sensor.VL6180X(i2c_port=sensor_i2c_port)
balance = balance.Balance(tty_port=balance_tty_port)

TSO_protocol = CAN.Protocol(interface_type=CAN_interface_type, 
                            arbitration_id=CAN_ID, 
                            bitrate=CAN_bitrate, 
                            time_base=CAN_time_base)

uarm.reset()

'''
while True:
    if TSO_protocol.condition_met():
        uarm.set_weight_to_somewhere(grab_position=vehicle_position, drop_position=balance_position, sensor=sensor, sensor_threshold=sensor_threshold)
        msg = balance.weigh()
        TSO_protocol.send(msg)
        buzzer.play_funky_town(frequency_multiplier=buzzer_frequency_multiplier, duration_multiplier=buzzer_duration_multiplier)
        uarm.set_weight_to_somewhere(grab_position=balance_position, drop_position=vehicle_position, sensor=sensor, sensor_threshold=sensor_threshold)
        buzzer.play_funky_town(frequency_multiplier=buzzer_frequency_multiplier, duration_multiplier=buzzer_duration_multiplier)
'''

# CAN protocol implementation rewrite.
CAN_message_received = None
time_base_in_milliseconds = float(TSO_protocol.time_base) * 1000.0

'''
ppid = os.getpid()
return_value = os.fork()
pid = os.getpid()

if return_value is 0: # child
    payload()
else: # parent
    CAN_loop()
'''

while True:
    CAN_message_received_old = CAN_message_received.copy()
    CAN_message_received = TSO_protocol.receive()

    timestamp = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    timestamp += datetime.datetime.timedelta(milliseconds=int(time_base_in_milliseconds) * (TSO_protocol.arbitration_id - 1))

    while True:
        if CAN_message_received is not None: # Message seen on CAN bus.
            if TSO_protocol.is_error(CAN_message_received):
                CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_RETRANSMIT)
                processes.kill()
                break
            if CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old)
                if unit is not None:
                    uarm.set_weight_to_somewhere(grab_position=vehicle_position, drop_position=balance_position, sensor=sensor, sensor_threshold=sensor_threshold)
                    weight = balance.weigh()
                    CAN_message_send = TSO_protocol.parse_balance_output(weight, unit)
                    uarm.set_weight_to_somewhere(grab_position=balance_position, drop_position=vehicle_position, sensor=sensor, sensor_threshold=sensor_threshold)
        timestamp_parsed = int(timestamp.milliseconds / time_base_in_milliseconds)
        timestamp_now = datetime.datetime.fromtimestamp(time.time())
        timestamp_now_parsed = int(timestamp_now.milliseconds / time_base_in_milliseconds)
        if timestamp_parsed > timestamp_now_parsed:
            CAN_message_send = TSO_protocol.set_error_message(CAN_message_received, error_code=TSO_protocol.ERROR_TIMESTAMP)
            processes.kill()
            break
        elif timestamp_parsed == timestamp_now_parsed:
            break
        else:
            continue

    TSO_protocol.send(CAN_message_send)

