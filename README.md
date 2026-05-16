## About

My attempt at building a virtual CAN Network to implement SecOC

## Implementation Details 

1. SecOC Profile 1 
   1. Algo = AES-128
   2. MAC = AEC-CMAC
   3. MAC size = 128bit
   4. MAC trunc size = 21 bits
   5. Fresheness size = 64 bits
   6. Freshnesss trunc size = 8 bits

MAC = AEC-CMAC( Key, Data | FV)

Frame layout:


## Setup

### Linux

Virtual CAN Setup

```
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

## Running Simulation

### Terminal 1 - raw vcan0

run candump to view raw traffic on vcan0 interface

```
candump vcan0
```

### Terminal 2 - ECU1

run python script for ECU1 from src directory

```
python -m ecu1.ecu1
```

### Terminal 3 - ECU22

run python script for ECU2 from src directory

```
python -m ecu2.ecu2
```