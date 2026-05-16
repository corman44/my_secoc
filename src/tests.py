import unittest
import os
from secoc import fvm as FVM, crypto, pdu
import time

class TestCMAC(unittest.TestCase):
    def test_cmac_gen(self):
        msg = bytes([0,1,2,3])
        key = bytes(range(16))
        cmac = crypto.trunc_cmac_gen(msg,0x00,key)

        print(f"Generated Trunc_CMAC: {cmac}")
        self.assertEqual(cmac, 3899428)

class TestFVM(unittest.TestCase):
    def test_fvm_counter(self):
        COUNT_UP_DOWN = 1
        fvm = FVM.FVM()
        msg_id = 0
        fvm.add_msg(msg_id)

        # test first 5 increments
        for i in range(COUNT_UP_DOWN):
            self.assertEqual(fvm.get_counter(msg_id), i)
            time.sleep(1)

        fvm.sync_counter(msg_id, 12345)
        for i in range(COUNT_UP_DOWN):
            self.assertEqual(fvm.get_counter(msg_id), i + 12345)
            time.sleep(1)

class TestPDU(unittest.TestCase):
    def test_encode_decode(self):
        pl = list(range(60)) 
        fv = 0xC0
        cmac = 0xACACAC
        enc = pdu.encode(pl, fv, cmac)
        self.assertEqual(len(enc), 64)
        self.assertEqual(enc[60], fv)
        self.assertEqual(int.from_bytes(enc[61:], 'big'), cmac)

        (d_pl, d_tfv, d_tcmac) = pdu.decode(enc)
        self.assertEqual(d_pl, bytes(pl))
        self.assertEqual(d_tfv, fv)
        self.assertEqual(d_tcmac, cmac)






if __name__ == "__main__":
    unittest.main()