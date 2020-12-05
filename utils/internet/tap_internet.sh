#!/bin/bash

# File:        utils/internet/tap_internet.sh
# By:          Samuel Duclos
# For:         My team.
# Description: Tap internet on a Linux device without internet from an existing 
#              wired connection to a Linux computer with internet access.
# Usage:       sudo bash utils/internet/tap_internet.sh <GATEWAY>
# Example:     sudo bash utils/internet/tap_internet.sh 192.168.7.1
# Note:        Repeat at each reboot.

/sbin/route add default gw 192.168.7.1
#/usr/sbin/ntpdate -b -s -u ie.pool.ntp.org
echo 'nameserver 8.8.8.8' >> /etc/resolv.conf
#echo 'nameserver 8.8.4.4' >> /etc/resolv.conf
