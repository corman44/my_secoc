import unittest
import os
from secoc import fvm as FVM ,crypto
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
        fvm = FVM.FVM()
        msg_id = 0
        fvm.add_msg(msg_id)

        # test first 5 increments
        for i in range(5):
            self.assertEqual(fvm.get_counter(msg_id), i)
            time.sleep(1)

        fvm.sync_counter(msg_id, 12345)
        for i in range(5):
            self.assertEqual(fvm.get_counter(msg_id), i + 12345)
            time.sleep(1)


if __name__ == "__main__":
    unittest.main()