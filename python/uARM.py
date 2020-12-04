#!/usr/bin/env python3

# File:        uARM.py
# By:          Samuel Duclos
# For:         My team.
# Description: uARM control in Python for TSO_team.
# TODO:      - parallelize processes:
#              1) while True:
#                  1) if CAN_message_received is not None:
#                      1) timestamp = time.time()
#                      2) if TSO_protocol.is_error(CAN_message_received):
#                          1) CAN_message_send = TSO_protocol.set_error_message(CAN_message_received)
#                          2) processes.kill() # (auto-cleanup should be ready)
#                          3) continue
#                      3) if CAN_message_received.arbitration_id == 1:
#                          1) unit = TSO_protocol.payload_received(CAN_message_received, CAN_message_received_old) # Black puck is ready.
#                          2) if unit is not None: # Black puck is ready.
#                              1) uarm.set_weight_to_somewhere(vehicle, balance, sensor, sensor_threshold) # (done)
#                              4) weight = balance.weigh()
#                              3) CAN_message_send = TSO_protocol.parse_balance_output(weight, unit) # AND-masked divided weight to lower byte, with unit bit set.
#                              4) uarm.set_weight_to_somewhere(balance, vehicle, sensor, sensor_threshold) # (done)
#                      4) if (time.time() - timestamp) <= 0:
#                          1) TSO_protocol.send(CAN_message_send)

from __future__ import print_function
from utils import balance, buzzer, CAN, sensor, uarm

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
def payload():
    while True:
        CAN_message_received_old = CAN_message_received.copy()
        CAN_message_received = TSO_protocol.receive()

        if CAN_message_received is not None: # Message seen on CAN bus.
            if CAN_message_received.arbitration_id == 1: # SYNC received from control bridge.
                time.sleep(TSO_protocol.time_base * (TSO_protocol.arbitration_id - 1)) # Wait for own turn.
                if CAN_message_received_old != CAN_message_received: # Fix this.
                    return (CAN_message_received.data[0] & 0x10) == 0x10 # TSO CAN protocol code for pick up object command.
            elif (CAN_message_received.data[0] & 0xE0) > 0x03:
                CAN_message_send = (CAN_message_send & 0x1F) | 0xE0
        return False
'''

