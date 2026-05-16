from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# Profile 1 CMAC Generation
# cmac = encrypt( payload + FV , key ) & 0x16777215 #Least Sig 24 bits of the 64bit MAC

def cmac_gen(payload, ffv, key):
    # ensure payload is <= 60 bytes
    if len(payload) > 60:
        print(f"Payload too long {len(payload)}") 

    # pad end until 60bytes payload reached

    # combine payload and ffv
    combined = bytes(payload) + bytes(ffv)

    cmac = CMAC.new(key, ciphermod=AES)
    cmac.update(combined)

    return cmac.digest()

def trunc_cmac_gen(payload, ffv, key):
    cmac = cmac_gen(payload, ffv, bytes(key))

    # truncate least sig 24-bits from cmac 32
    # print(f"CMAC: {cmac}")
    trunc_cmac = int.from_bytes(cmac[-3:], 'big')

    return trunc_cmac
