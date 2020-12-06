#!/usr/bin/env python3

# File:          python/uARM_object_scan_test.py
# By:            Samuel Duclos
# For:           My team.
# Description:   Test uARM for object detection using I2C VL6180X Time-of-Flight sensor to scan until object is found.
# For help:      python3 python/uARM_object_scan_test.py --help # <-- Use --help for help using this file like this. <--

from __future__ import print_function
from utils import sensor, uarm


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
    parser.add_argument('--speed', metavar='<speed>', type=int, required=False, default=150, help='Speed of uARM displacements.')
    parser.add_argument('--uarm-tty-port', metavar='<uarm-tty-port>', type=str, required=False, default='/dev/ttyUSB1', help='uARM UART TTY port.')
    parser.add_argument('--sensor-i2c-port', metavar='<sensor-i2c-port>', type=int, required=False, default=1, help='I2C port for Time-of-Flight (VL6180X) sensor.')
    parser.add_argument('--sensor-threshold', metavar='<sensor-threshold>', type=float, required=False, default=0.5, help='VL6180X sensor threshold for object detection.')
    parser.add_argument('--uart-delay', metavar='<uart-delay>', type=float, required=False, default=2.0, help='Delay after configuring uARM\'s UART port.')
    parser.add_argument('--grab-delay', metavar='<grab-delay>', type=float, required=False, default=5.0, help='Delay after uARM grabs object.')
    parser.add_argument('--drop-delay', metavar='<drop-delay>', type=float, required=False, default=5.0, help='Delay after uARM drops object.')
    parser.add_argument('--pump-delay', metavar='<pump-delay>', type=float, required=False, default=5.0, help='Delay after uARM (de-)pumps object.')
    parser.add_argument('--servo-attach-delay', metavar='<servo-attach-delay>', type=float, required=False, default=5.0, help='Delay after uARM detaches servos.')
    parser.add_argument('--set-position-delay', metavar='<set-position-delay>', type=float, required=False, default=5.0, help='Delay after uARM set to position.')
    parser.add_argument('--servo-detach-delay', metavar='<servo-detach-delay>', type=float, required=False, default=5.0, help='Delay after uARM attaches servos.')
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

    # Do relative positioning loop here.

if __name__ == '__main__':
    main()

