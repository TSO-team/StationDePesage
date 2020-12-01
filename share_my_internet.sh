#!/bin/sh
# Share one network's internet connection with another network.
# eg: If your Wifi adapter with internet is called wlan0
# and your local Ethernet adapter is called eth0,
# then run:
#    ./share_my_internet.sh wlan0 eth0
# This will only last until you reboot your computer.
sudo iptables --flush
sudo iptables --table nat --flush
sudo iptables --delete-chain
sudo iptables --table nat --delete-chain
sudo iptables --table nat --append POSTROUTING --out-interface $1 -j MASQUERADE
sudo iptables --append FORWARD --in-interface $2 -j ACCEPT
sudo sysctl -w net.ipv4.ip_forward=1
