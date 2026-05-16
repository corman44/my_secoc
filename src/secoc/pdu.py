"""
PDU Layout
- 64 byte Frame
- first 60 bytes are payload
- last 4 bytes are TFV and TCMAC
 - 8 bits of TFV + 24bits of TCMAC
"""

PAYLOAD_LEN = 60
TFV_LEN = 1
TCMAC_LEN = 3
FRAME_LEN = 64

def encode(payload, trunc_fv, trunc_cmac) -> bytes:
    if len(payload) > PAYLOAD_LEN:
        raise ValueError(len(payload))
    if len(payload) < PAYLOAD_LEN:
        for i in range(PAYLOAD_LEN - len(payload)):
            payload.append(0)
    
    return bytes(list(payload) + [trunc_fv] + list(trunc_cmac.to_bytes(3, 'big')))

def decode(frame: bytes) -> tuple:
    payload = frame[:60]
    trunc_fv = frame[60]
    trunc_cmac = frame[61:64]
    return (payload, trunc_fv, int.from_bytes(trunc_cmac, 'big'))
