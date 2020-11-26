import time
import can

bustype = 'vcan0'

bus = can.interface.ThreadSafeBus(channel='socketcan', bustype=bustype)
msg = can.Message(arbitration_id=003, data=[0x40, 0xAA], is_extended_id=False)
bus.send(msg)
time.sleep(1)
