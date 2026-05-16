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
    msg1_id = 0xCC

    fvm = FVM.FVM()
    fvm.add_msg(msg1_id)
    secret_key = list(range(16))
    print(f"ECU2 secret_key: {secret_key}")

    while(1):
        msg = bus.recv()
        (pl, tfv, tcmac) = pdu.decode(msg.data)

        fvm.sync_counter(msg.arbitration_id, tfv)
        gen_tcmac = crypto.trunc_cmac_gen(pl, fvm.get_counter(msg.arbitration_id), secret_key)

        print(f"RX CMAC: {tcmac}, Gen CMAC: {gen_tcmac}")

    pass