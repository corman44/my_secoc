from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# Profile 1 CMAC Generation
# cmac = encrypt( payload + FV , key ) & 0x16777215 #Least Sig 24 bits of the 64bit MAC

def cmac_gen(payload, ffv, key):
    # ensure payload is <= 60 bytes

    # pad end until 60bytes payload reached

    # combine payload and ffv
    combined = payload + ffv

    cmac = CMAC.new(key, ciphermod=AES)
    cmac.update(combined)

    return cmac.hexdigest()

def trunc_cmac_gen(payload, ffv, key):
    cmac = cmac_gen(payload, ffv, key)

    # truncate least sig 24-bits from cmac 32
    print(f"CMAC: {cmac}")
    last4 = bytes(cmac[-4:], encoding='utf-8')
    print(f"last4: {last4.decode('utf-8')}")
    
    trunc_cmac = 0
    for i in range(4):
        trunc_cmac |= last4[-i] << i-1

    print(trunc_cmac)
