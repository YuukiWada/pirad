# PiRAD

## Overview
PiRAD is a radiation detector using Raspberry Pi. It allows for the acquisition of information for each photon of X-rays and gamma rays (energy and arrival time), as well as functions such as supplying high voltage for MPPCs (Multi-Pixel Photon Counters) and temperature compensation for MPPCs, all while being inexpensive and simple.

This software and design information are distributed under the GPL (GNU General Public License version 3). The developer bears no responsibility for any troubles, losses, or damages arising from the use of this software or design information.

## Usage
PiRAD consists of an analog circuit board to be stacked on Raspberry Pi and software running on Raspberry Pi.

### Circuit Board
The `circuit` directory contains Gerber files and parts lists necessary to manufacture the PCB. Please use this information to fabricate the PCB and implement the components on the board. The PCB is a 4-layer board with dimensions of 105 mm × 56 mm. It includes provisions for mounter implementation and requires V-cut. Mounter reference markers are also provided.

### Data Acquisition Software
Data acquisition software is stored in the `scripts` directory. These are composed of C, Python, and Ruby languages. The software has been tested on Raspberry Pi4 Model B with Raspberry Pi OS with Desktop 32-bit Brookworm. 64-bit OS is not supported.

## Developer Information
Yuuki Wada (Assistant Professor, Department of Electrical, Electronic, and Infocommunications Engineering, Graduate School of Engineering, Osaka University)
