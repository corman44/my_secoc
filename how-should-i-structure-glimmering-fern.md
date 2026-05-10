# Plan: Freshness Value (FV) Structure for SecOC

## Context

The current `crypto.py` stub shows Profile 1 CMAC generation but has no freshness value logic. In AUTOSAR SecOC, the Freshness Value Manager (FVM) is a distinct module from the crypto layer — it owns all counter state and provides FVs on demand. This separation needs to be established before the MAC computation can be wired up end-to-end.

---

## AUTOSAR FVM Concepts (what to model)

**Full Freshness Value (FFV):** A wide counter (e.g., 64-bit) maintained internally. The MAC is always computed over the full value — never the truncated one. This is the replay-prevention guarantee.

**Truncated Freshness Value (TFV):** The lower N bits of the FFV sent on the wire to save bandwidth. The receiver uses it to reconstruct the FFV.

**Receiver reconstruction:** The receiver keeps its own stored FFV. When it receives a TFV, it reconstructs the FFV by:
1. If `received_tfv > lower_bits(stored_ffv)`: FFV = `upper_bits(stored_ffv) | received_tfv` (counter moved forward in same window)
2. If `received_tfv <= lower_bits(stored_ffv)`: FFV = `(upper_bits(stored_ffv) + 1 window) | received_tfv` (counter wrapped into next window)
3. An **acceptance window** defines how many increments ahead the receiver will tolerate (prevents infinite lookahead).

---

## Proposed Module Structure

### New file: `src/secoc/fvm.py`

This module is the Freshness Value Manager. It should:
- Maintain a dictionary of `{msg_id: full_freshness_value}` (one counter per message ID, since each PDU has its own FV in AUTOSAR)
- Expose a method to get the current full FV for MAC computation
- Expose a method to get the truncated FV for wire transmission
- Expose a method to increment the counter (called by sender after a successful send)
- Expose a method to reconstruct the full FV from a received truncated value (called by receiver before MAC verification)

### Updated: `src/secoc/crypto.py`

The MAC generation function takes `(payload, full_freshness_value, key)` — it should never touch the FVM directly. The separation keeps crypto pure and testable.

### Updated: `src/main.py`

The sender flow becomes:
1. FVM: get full FV for this msg_id
2. Crypto: compute MAC over `payload + full_fv`
3. FVM: get truncated FV for this msg_id
4. Build SecOC PDU: `[payload | truncated_fv | mac_truncated]`
5. Send on vcan0
6. FVM: increment counter for this msg_id

---

## Key Design Decisions to Make

| Decision | Options | Recommendation |
|---|---|---|
| FV bit width | 16, 32, 64 bits | 64-bit internally; truncate to 4 or 8 bits on the wire for visibility |
| Truncated FV width | 4–32 bits | 4 bits (1 nibble) makes replay attacks easy to observe in candump |
| Counter scope | Global vs. per msg_id | Per msg_id — matches AUTOSAR and lets you simulate multiple ECUs |
| Persistence | In-memory only | Fine for simulation; note that a real system would persist to NvM |
| Acceptance window | Fixed integer N | Start with N=15 (fill the nibble); makes the reconstruction logic obvious |

---

## Files to Create/Modify

| File | Action |
|---|---|
| `src/secoc/fvm.py` | Create — FreshnessValueManager class |
| `src/secoc/crypto.py` | Flesh out — MAC function takes full FV as a parameter |
| `src/main.py` | Update — sender flow wires FVM → crypto → PDU build |

---

## Verification

- Run `python src/main.py` and watch `candump vcan0` — the PDU bytes should include the truncated FV nibble changing on each send
- Manually increment the FVM counter past a nibble boundary (value 15→16) and confirm the reconstruction logic returns the correct full FFV on the receiver side
- Set a wrong key and confirm the MAC bytes in the PDU change (proving the MAC covers the FV)
