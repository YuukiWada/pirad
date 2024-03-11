# PiRAD

## Overview
PiRAD is a radiation detector using Raspberry Pi. It allows for the acquisition of information for each photon of X-rays and gamma rays (energy and arrival time), as well as functions such as supplying high voltage for MPPCs (Multi-Pixel Photon Counters) and temperature compensation for MPPCs, all while being inexpensive and simple.

This software and design information are distributed under the GPL (GNU General Public License version 3). The developer bears no responsibility for any troubles, losses, or damages arising from the use of this software or design information.

## Usage
PiRAD consists of an analog circuit board that is stacked on the Raspberry Pi and software that runs on the Raspberry Pi.

### Things to prepare
- Raspberry Pi 4B+ (any memory capacity allowed)
- PiRAD board
- MPPC/SiPM, Scintillator, Coaxial cable
- AC adapter of 5 V and >2 A
- microSD card (16 GB or higher, Class 10 recommended)
- USB memory

### Circuit board
The `circuit` directory contains Gerber files and parts lists needed to fabricate a PCB board. Please use this information to produce the PCB board and mount the components on the board. The PCB board is a 4-layer board with dimensions of 105 mm x 56 mm. A disposable board is attached so that it can be fed into a chip mounter. V-cut is required. A reference marker for the chip mounter is also placed.

LT3482IUDTRPBF is used as the HV supplier chip. Please note that this chip has pads for surface mounting on the back side of the component, so placing components by a chip mounter may be required. In that case, it is necessary to manufacture a metal mask, which requires initial costs and is expensive if produced in small quantities. An effective method for small-volume production is to manufacture the boards without LT3482IUDTRPBF, and then manually mount it later manually. However, this is only possible if you have the technology to perform surface mounting using a heat gun and solder paste.

### Radiation detection section
This part is left to the user's choice. In the author's test environment, Hamamatsu's MPPC/SiPM S13360-6050CS is used, and a 1 x 1 x 1 cm GAGG scintillator is attached to the MPPC. The HV supply mounted on the circuit board has positive polarity, so supply voltage to the cathode and connect the anode to GND. In the author's environment, the MPPC is connected to the circuit board using a coaxial cable with an SMA terminal.

### Data Acquisition Software
The data acquisition software is stored in `scripts`. They consist of three languages: C, Python, and Ruby. Software operation has been confirmed on Raspberry Pi4 Model B and Raspberry Pi OS with Desktop 32-bit brookworm. 64-bit OS is not supported.

Please refer to `INSTALL.md` for how to set up the software.

### Radiation data acquisition
Once you have finished configuring the software, write the configuration file to a USB memory and insert it to the Raspberri Pi. Please refer to `INSTALL.md` for the configuration file settings.

After inserting the USB and turning on the Raspberry Pi, the PWR LED will light up. Observation can begin after the PWR LED turns on. By turning on the LOGGING slide switch, the USB memory will be mounted and observation will begin. If the USB memory cannot be read or is not correctly mounted, the LOG LED will blink twice.

If the USB memory is mounted successfully and the configuration file is also successfully read, the HV/LOG LED will light up and measurement will begin. If radiation is detected, the RAD LED will blink.

When a GPS module is connected and time synchronization is set, the GPS LED will light up while the time is synchronized by GPS acquisition.

To stop measurement, turn off the LOGGING slide switch. The HV/LOG LED will turn off within a few seconds. After that, the LOG LED will blink 5 times and the USB will be unmounted and you can safely remove it from the Raspberry Pi.

To shut down, press and hold the PWR OFF switch until the PWR LED turns off. Wait a few seconds for the shutdown process to complete. Please note that if you stop the power supply without performing the shutdown process, the SD card may not be read properly and you may not be able to start it up again.

### data format
Data is recorded in USB memory. Radiation data is recorded as text in CSV format, and the file name is the measurement start time (UTC). Inside the file is recorded as follows.
````
1710139818.021942
0.000070, 410
0.395692, 73
1.175464, 88
1.209030, 88
1.948140, 94
2.283456, 67
2.334519, 144
````
 The first line is the reference time (UNIXTIME), the second and subsequent lines correspond to the detected radiation event, the first column is the elapsed time (seconds) from the reference time, and the second column is the peak value (pulse height). Conversion from peak value to energy requires calibration using a radiation source, etc. The files are separated by day and are switched around 0:00 UTC (9:00 Japan Standard Time / JST).

HK (housekeeping) data is also saved with the recording start time as the file name, and is recorded as follows.

````
1706767240, 2024-02-01 06:00:40, 54.49946, 24.99, 30.12, 1011.96
1706767540, 2024-02-01 06:05:40, 54.49946, 24.83, 30.36, 1011.89
1706767840, 2024-02-01 06:10:40, 54.49946, 24.77, 30.31, 1011.87
1706768140, 2024-02-01 06:15:40, 54.49946, 24.91, 30.12, 1011.88
````
The first column is UNIXTIME, the second column is the corresponding time (UTC), the third column is the actual applied high voltage value, the fourth column is temperature, the fifth column is humidity, and the sixth column is atmospheric pressure. Note that if the HV's temperature compensation is turned off (including the case where the temperature sensor is not connected), the temperature, humidity, and pressure will not be recorded. Similarly, HK data files are separated by day, and are switched around 0:00 UTC (9:00 Japan time).


## Developer Information
Yuuki Wada (Assistant Professor, Department of Electrical, Electronic, and Infocommunications Engineering, Graduate School of Engineering, Osaka University)

## Update information
First edition: February 2, 2024
Second edition: March 11, 2024