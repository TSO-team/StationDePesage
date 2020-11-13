#!/bin/bash

/sbin/route add default gw 192.168.7.1
/usr/sbin/ntpdate -b -s -u ie.pool.ntp.org
echo 'nameserver 8.8.8.8' >> /etc/resolv.conf
