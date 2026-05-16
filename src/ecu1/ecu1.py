import can
from secoc import crypto, fvm as FVM, pdu
from os import urandom
from time import sleep

if __name__ == "__main__":
    bus = can.interface.Bus(
        channel='vcan0',
        interface='socketcan',
        fd=True
    )

    msg1 = can.Message(
        arbitration_id = 0xCC,
        is_extended_id=False,
        is_fd=True,
        bitrate_switch=True
    )

    fvm = FVM.FVM()
    fvm.add_msg(msg1.arbitration_id)
    pl = bytes(range(60))
    secret_key = list(range(16))
    print(f"ECU1 secret_key: {secret_key}")

    while(1):
        count = fvm.get_counter(msg1.arbitration_id)
        tcmac = crypto.trunc_cmac_gen(pl, count, secret_key)
        my_pdu = pdu.encode(pl, count, tcmac)

        msg1.data = my_pdu
        bus.send(msg1)

        sleep(5)

    pass