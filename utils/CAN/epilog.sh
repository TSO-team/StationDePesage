#!/bin/bash

# File:        utils/CAN/epilog.sh
# By:          Samuel Duclos
# For:         My team.
# Description: Post-deconfigures CAN.
# Usage:       sudo bash utils/CAN/epilog.sh vcan
#              ... where "vcan" is the INTERFACE_TYPE (one of "vcan" or "can").

# Parse and set arguments from command-line.
INTERFACE_TYPE=$(echo "${1:-vcan}" | tr '[:lower:]' '[:upper:]')
INTERFACE="${INTERFACE_TYPE}0"

# Destroy network interface.
ip link set down $INTERFACE
ip link delete dev $INTERFACE type $INTERFACE_TYPE
