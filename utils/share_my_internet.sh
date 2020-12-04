#!/bin/bash

# Share one network's internet connection with another network.
# eg: If your Wifi adapter with internet is called wlan0
# and your local Ethernet adapter is called eth0,
# then run:
#    sudo bash share_my_internet.sh wlan0 eth0
# This will only last until you reboot your computer.

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface $1 -j MASQUERADE
iptables --append FORWARD --in-interface $2 -j ACCEPT
sysctl -w net.ipv4.ip_forward=1
