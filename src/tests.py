import unittest
import os
from secoc import fvm,crypto

class TestCMAC(unittest.TestCase):
    def test_cmac_gen(self):
        known_cmac = []
        msg = bytes([0,1,2,3])
        key = bytes(range(16))
        #cmac = crypto.cmac_gen(msg,b"0",key)
        cmac = crypto.trunc_cmac_gen(msg,b'0',key)

        print(f"CMAC: {cmac}")

        # self.assertEqual(cmac, known_cmac)

if __name__ == "__main__":
    unittest.main()