# PortScanner

## Overview
PortScanner is a simple and efficient port scanner written in Python, utilizing only standard libraries.

## Features
- Scan a range of ports on a target IP address.
- Choose between TCP and UDP scanning.
- Multi-threaded scanning for faster results.
- Optional logging of results to a file.

## Usage
### Arguments
- `target`: IP address of the system to scan.
- `port`: Range of ports to scan (e.g., 20-80).
- `threads`: Number of CPU threads to use for scanning.
- `udp`: Use UDP instead of TCP for scanning (set to `True` for UDP, `False` for TCP).
- `verbose`: Log the results to a file (set to `True` to enable logging).

### Example
```bash
python3 main.py -target 192.168.1.1 -p 20-80 -t 4 -u False -v True
```

## Installation
```bash
git clone https://github.com/FjoGeo/portscanner.git
cd portscanner
```