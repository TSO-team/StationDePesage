#!/bin/bash

# File:        io/balance.sh
# By:          Samuel Duclos
# For:         My team.
# Description: Outputs current weight from balance to UART.

if [ "$#" -ne 1 ]; then
    echo "Usage: "
    echo "    sudo bash io/balance.sh &"
    exit
else
    #TTY=/dev/ttyUSB0
    #TTY=/dev/ttyO3
    TTY=$1

cat -v < $TTY &
PID=$!
echo -ne "T\n\r" > $TTY
sleep 1
echo -ne "Z\n\r" > $TTY
sleep 1
echo -ne "P\n\r" > $TTY
sleep 5
echo -ne "T13.37\n\r" > $TTY
sleep 1
echo -ne "P\n\r" > $TTY
sleep 5

kill $PID > /dev/null
exit 0