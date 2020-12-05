#!/bin/bash

# File:        utils/internet/share_internet.sh
# By:          Samuel Duclos
# For:         My team.
# Description: Share internet through existing wired connection 
#              from a Linux computer to a Linux device without internet.
# Usage:       sudo bash utils/internet/share_internet.sh <HOST> <DEVICE>
# Example:     sudo bash utils/internet/share_internet.sh wlan0 eth0
# Note:        Repeat at each reboot.

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface $1 -j MASQUERADE
iptables --append FORWARD --in-interface $2 -j ACCEPT
sysctl -w net.ipv4.ip_forward=1
