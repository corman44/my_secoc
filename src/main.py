import can

bus = can.interface.Bus(channel='vcan0', interface='socketcan')

msg = can.Message(
    arbitration_id=0x123,
    data=[0x01, 0x02, 0x03, 0x04, 0x05],
    is_extended_id=False
)

try:
    bus.send(msg)
    print(f"Message sent on {bus.channel_info}")
except can.CanError:
    print("Message NOT sent")