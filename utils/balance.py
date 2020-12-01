#!/usr/bin/env python3

# File:        utils/balance.py
# By:          Samuel Duclos
# For:         My team.
# Description: Outputs current weight from balance.

from __future__ import print_function
import subprocess, time

balance_tty_port = '/dev/ttyO3'

def weigh(balance_tty_port='/dev/ttyO3'):
    subprocess.run('echo -ne "T\n\r" > ' + balance_tty_port, stderr=subprocess.STDOUT, shell=True)
    time.sleep(1)
    subprocess.run('echo -ne "Z\n\r" > ' + balance_tty_port, stderr=subprocess.STDOUT, shell=True)
    time.sleep(1)
    subprocess.check_output('echo -ne "P\n\r" > ' + balance_tty_port, stderr=subprocess.STDOUT, shell=True)
    time.sleep(5)
    

