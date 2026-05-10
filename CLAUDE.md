# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A virtual CAN network implementation of SecOC (Secure Onboard Communication), the AUTOSAR standard for authenticating CAN messages using MACs. The goal is to simulate an ECU network with message authentication on Linux using `vcan`.

## Purpose

Educational implmentation of SecOC using Virtual CAN interface. I want to learn how to implement this. Claude should only propose changes to approach, structure, or layout but not actually implement anything.

## Setup

### Linux — Virtual CAN Interface

Run once per boot before using the project:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

### Python Dependencies

```bash
pip install python-can
```

## Running

```bash
python src/main.py
```

Monitor the vcan bus (separate terminal):

```bash
candump vcan0
```


## Architecture

**`src/main.py`** — sends a raw CAN frame on `vcan0` via `python-can`. Entry point for testing the bus.

**`src/secoc/crypto.py`** — SecOC cryptographic primitives. Currently implements **Profile 1 CMAC generation**:
- MAC = `encrypt(payload + FreshValue, key)`, truncated to the least-significant 24 bits of the 64-bit output.
- FreshValue (FV) is the freshness counter used to prevent replay attacks.

The SecOC flow follows AUTOSAR: sender appends a truncated MAC + freshness value to the PDU; receiver recomputes and verifies before processing the payload.
