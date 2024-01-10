# XDAQ IO Expander Demo
## Overview
The XDAQ IO Expander example provides a concise demonstration of pyxdaq functionality tailored for communication with the IO expander. This stripped-down version of our pyxdaq library serves as a guide for integrating the XDAQ IO Expander into your own code.

## Features
The XDAQ IO Expander enhances the I/O capabilities of our XDAQ systems, supporting up to 8 analog inputs, 8 analog outputs, 32 digital inputs, and 32 digital outputs. This surpasses the limitations of the Intan Data format, which is limited to 8 analog I/O pairs and 16 digital I/O pairs.

## Data Format
To accommodate the expanded I/O, our XDAQ systems employ a custom data format distinct from the Intan Data format. By default, this extended data format is disabled to ensure compatibility with existing systems.

## Demo Purpose
This demonstration illustrates how to enable the extended data format and retrieve the additional data from the IO Expander.

## Additional Resources
* [KonteX XDAQ IO Expander](https://kontex.io/collections/xdaq/products/xdaq-io-expander)
* Related source code at XDAQ-OE (XDAQ OpenEphys Plugin)
    * [Expander detection](https://github.com/open-ephys-plugins/XDAQ-OE/blob/f4793f4a9c057d69a282a74015980feaeea39c98/Source/rhythm-api/rhd2000evalboard.cpp#L378)
    * [Enable extended data format](https://github.com/open-ephys-plugins/XDAQ-OE/blob/f4793f4a9c057d69a282a74015980feaeea39c98/Source/rhythm-api/rhd2000evalboard.cpp#L199)
    * [Data frame parsing](https://github.com/open-ephys-plugins/XDAQ-OE/blob/f4793f4a9c057d69a282a74015980feaeea39c98/Source/rhythm-api/rhd2000datablock.h#L62)

## Installation
### Prerequisites
* [Git](https://git-scm.com/)
* [Python](https://www.python.org/downloads/) 3.8 or higher

### macOS
```shell
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install .
```

### Windows
```powershell
python --version # check that Python 3.8 or higher is installed
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install .
```

## Running the demo
```shell
python3 io_expander_demo.py # see example_output.txt for expected output
```
