#!/usr/bin/env python3

# File:          python/uARM_payload.py
# By:            Samuel Duclos
# For:           My team.
# Description:   Test uARM for object detection using I2C VL6180X Time-of-Flight sensor to scan until object is found.
# For help:      python3 python/uARM_payload.py --help # <-- Use --help for help using this file like this. <--
# TODO:          Output weight to parent.

from __future__ import print_function
from utils import balance, buzzer, sensor, uarm

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
    return parser.parse_args()

def main():
    import argparse
    args = parse_args()
    print(vars(args))

    first_position = {'x': args.first_x_position, 'y': args.first_y_position, 'z': args.first_z_position, 'speed': args.speed, 'relative': False, 'wait': True}
    second_position = {'x': args.second_x_position, 'y': args.second_y_position, 'z': args.second_z_position, 'speed': args.speed, 'relative': False, 'wait': True}
    third_position = {'x': args.third_x_position, 'y': args.third_y_position, 'z': args.third_z_position, 'speed': args.speed, 'relative': False, 'wait': True}

    uarm = uarm.UARM(uarm_tty_port=args.uarm_tty_port, 
                     uart_delay=args.uart_delay, 
                     initial_position=args.first_position, 
                     servo_attach_delay=args.servo_attach_delay, 
                     set_position_delay=args.set_position_delay, 
                     servo_detach_delay=args.servo_detach_delay, 
                     pump_delay=args.pump_delay)

    buzzer = buzzer.Buzzer(uarm=uarm.uarm, servo_detach_delay=uarm.servo_detach_delay, transition_delay=transition_delay)
    sensor = sensor.VL6180X(i2c_port=sensor_i2c_port)
    balance = balance.Balance(tty_port=balance_tty_port)
    uarm.reset()

    uarm.set_weight_to_somewhere(grab_position=args.second_position, drop_position=args.third_position, sensor=sensor, sensor_threshold=args.sensor_threshold)
    buzzer.play_funky_town(frequency_multiplier=buzzer_frequency_multiplier, duration_multiplier=buzzer_duration_multiplier)
    weight = balance.weigh()
    uarm.set_weight_to_somewhere(grab_position=balance_position, drop_position=vehicle_position, sensor=sensor, sensor_threshold=sensor_threshold)
    buzzer.play_funky_town(frequency_multiplier=buzzer_frequency_multiplier, duration_multiplier=buzzer_duration_multiplier)
    print(weight) # Output weight to parent.

if __name__ == '__main__':
    main()

