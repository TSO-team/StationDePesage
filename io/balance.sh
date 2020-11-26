#!/bin/bash
# balance.sh

cat -v < /dev/ttyUSB0 &
PID=$!
echo -ne "T\n\r" > /dev/ttyUSB0
sleep 1
echo -ne "Z\n\r" > /dev/ttyUSB0
sleep 1
echo -ne "P\n\r" > /dev/ttyUSB0
sleep 5
echo -ne "T13.37\n\r" > /dev/ttyUSB0
sleep 1
echo -ne "P\n\r" > /dev/ttyUSB0
sleep 5
kill $PID > /dev/null
