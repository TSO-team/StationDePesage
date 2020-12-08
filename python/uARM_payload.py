#!/usr/bin/env python3

# File:          python/uARM_payload.py
# By:            Samuel Duclos
# For:           My team.
# Description:   Do what the setup is made for...
# For help:      python3 python/uARM_payload.py --help # <-- Use --help for help using this file like this. <--

from __future__ import print_function
from utils import payload

def main():
    parser = argparse.ArgumentParser(description='Test uARM for object detection using I2C VL6180X Time-of-Flight sensor to scan until object is found.', 
                                     formatter_class=argparse.RawTextHelpFormatter)
    args = payload.add_payload_args()
    print(vars(args))

    payload = Payload(initial_x_position=args.initial_x_position, 
                      initial_y_position=args.initial_y_position, 
                      initial_z_position=args.initial_z_position, 
                      vehicle_x_position=args.vehicle_x_position, 
                      vehicle_y_position=args.vehicle_y_position, 
                      vehicle_z_position=args.vehicle_z_position, 
                      balance_x_position=args.balance_x_position, 
                      balance_y_position=args.balance_y_position, 
                      balance_z_position=args.balance_z_position, 
                      uarm_speed=args.uarm_speed, 
                      sensor_i2c_port=args.sensor_i2c_port, 
                      sensor_threshold=args.sensor_threshold, 
                      buzzer_frequency_multiplier=args.buzzer_frequency_multiplier, 
                      buzzer_duration_multiplier=args.buzzer_duration_multiplier, 
                      uarm_tty_port=args.uarm_tty_port, 
                      balance_tty_port=args.balance_tty_port, 
                      uart_delay=args.uart_delay, 
                      servo_attach_delay=args.servo_attach_delay, 
                      set_position_delay=args.set_position_delay, 
                      servo_detach_delay=args.servo_detach_delay, 
                      pump_delay=args.pump_delay, 
                      transition_delay=args.transition_delay, 
                      scan_x_displacement=args.scan_x_displacement, 
                      scan_y_displacement=args.scan_y_displacement, 
                      scan_z_displacement=args.scan_z_displacement, 
                      stride_x=args.stride_x, 
                      stride_y=args.stride_y, 
                      stride_z=args.stride_z)

    payload.payload()

if __name__ == '__main__':
    main()

