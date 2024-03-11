# How to install PiRAD software

## overview
This page describes how to install the software for Raspberry Pi used with PiRAD. Please note that this software is designed to operate on Raspberry Pi 4B+ and has not been tested on other Raspberry Pi versions. It also assumes an environment where you can access the Raspberry Pi via SSH.

## Things to prepare
- Raspberry Pi 4B+
- microSD card (16GB or higher, Class 10 recommended)
- Power supply for Raspberry Pi
- USB memory (formatted as FAT32)
- PC for configuration (the author uses macOS)

## Installation steps

### Preparing the SD card
First, write the OS for Raspberry Pi onto the SD card. Please use Raspberry Pi Imager for writing. Download and install the corresponding software from [here](https://www.raspberrypi.com/software/).

Insert the SD card into your PC and write the OS using Raspberry Pi Imager. Select Raspberry Pi 4 for Raspberry Pi Device and Raspberry Pi OS (32-bit) Debian Bookworm with the Raspberry Pi Desktop for OS. <span style="color: red;">Please be sure to select 32-bit. </span>

![Raspberry Pi Imager](images/imager.png)

After selecting the SD card to write to, you will be asked about customizing the OS, so select "Change settings". Set your username and password on the settings screen. The username here is pi. Check "Enable SSH" on the Services tab. Once the settings are complete, start writing.

### OS preparation
Insert the SD card into the Raspberry Pi. Make sure it is connected to the network via wired LAN, and supply power to Raspberry Pi. Check the IP address assigned to Raspberry Pi on your router, etc.

Access the Raspberry Pi via SSH. An example command is below.
````
ssh pi@192.168.1.2
````
Usernames and IP addresses will vary depending on each configuration environment.

Next, configure GPIO settings. Enter
````
sudo raspi-config
````
 to open the settings screen. Select "Interface Options" and enable SPI, I2C, and Serial Port. You may also change the time zone, etc., if necessary. The time zone is set to GMT by default.

Although not required, it is a good idea to implement public key authentication.
````
mkdir ~/.ssh
cd ~/.ssh/
nano authorized_keys
````
If you enter the public key in `authorized_keys`, you will be able to log in without entering a password next time.

### Clone and install software
First, clone the source code from GitHub.
````
mkdir ~/git
cd ~/git
git clone https://github.com/YuukiWada/pirad
cd pirad
````

Compile the DAQ software.
````
cd ~/git/pirad/scripts/c_lang
bash ./make.sh
````
If no error messages are displayed, the compilation was successful.

Next, install the software required for the script to run.
````
sudo apt install -y ruby ruby-dev openssl libssl-dev
sudo apt install -y python3-smbus python3-smbus2 python3-bme280 python3-yaml
````

Next, configure the crontab. Add the contents of
````
~/git/pirad/scripts/crontab_setting.txt
````
to the crontab after opening crontab editor by the command below.

````
sudo crontab -e
````

Then restart Raspberry Pi.
````
sudo reboot
````
If the settings are successful, the PWR LED will turn on after rebooting.

### Preparing the USB memory
When using PiRAD on a daily basis, it reads configuration files from a USB memory and also writes observation data directly to the USB memory so that there is no need to access the Raspberry Pi. Please format the USB memory as FAT32.

Please store [config.yaml](https://github.com/YuukiWada/pirad/blob/main/scripts/config.yaml) in the top directory of the USB memory. The content of the configuration file is as below.
````
hv: 56.0
threshold: 10
compensation: off
temp_const: 0.054
hv_limit: 60
````
From the top, the HV setting value, DAQ threshold, presence or absence of temperature compensation for the high voltage supplied to the MPPC, MPPC temperature coefficient [V/degC], and HV upper limit are listed. If a temperature sensor is not installed, turn compensation off.

Insert the USB memory with the configuration file into the Raspberry Pi. If the USB memory is compatible with USB3.0, recommend inserting it into a USB3.0 port.

Turn on the LOGGING switch and wait a few seconds, the HV LED will turn on, followed by the LOG LED, and when radiation is observed, the RAD LED will blink.

### Setting up time synchronization using GPS
If a GPS module is connected, time synchronization using GPS is possible even offline.

Enter
````
sudo nano /boot/cmdline.txt
````
and comment out all the lines with # and instead
````
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
````


Then, open
````
sudo nano /boot/config.txt
````
and add
````
init_uart_baud=9600
dtoverlay=pps-gpio,gpiopin=4,assert_falling_edge=true
````
in the last line. `assert_falling_edge` varies depending on the GPS module used; select true if PPS is a falling pulse (active low) and false if it is a rising pulse (active high).

Also, to recognize PPS input, execute the command below.
````
echo pps-gpio | sudo tee -a /etc/modules
````
Then,  restart Raspberry Pi.
````
sudo reboot
````

Install the required software after rebooting.
````
sudo apt install -y gpsd gpsd-clients pps-tools
````

Next is the gpsd settings. Open the configuration file as
````
sudo nano /etc/default/gpsd
````
and add
````
START_DAEMON="true"
DEVICES="/dev/ttyS0 /dev/pps0"
GPSD_OPTIONS="-n"
````
in the last line. Then, activate with the command below.
````
sudo systemctl enable gpsd.socket
````
If the GPS signal can be received, you can check the GPS signal with the following command.
````
gpsmon
sudo ppstest /dev/pps0
````

Install chrony as NTP software.
````
sudo apt -y install chrony
````

To change chrony settings, open the configuration file with
````
sudo nano /etc/chrony/chrony.conf
````
comment out
````
sourcedir /run/chrony-dhcp
````
with #, and add
````
refclock PPS /dev/pps0 lock NMEA refid GPS
````
in the last line. Then, beboot the system with

````
sudo systemctl restart chrony.service
````

You can check the NTP status with
````
chronyc sources -v
````
When the time is synchronized by GPS, the GPS LED lights up.

## Advanced settings

### I2C address ofTemperature sensor 
The temperature sensor is communicating via I2C. Operation has been confirmed using [Akizuki Denshi's AE-BME280] (https://akizukidenshi.com/catalog/g/g109421/). Its I2C address is 0x76.

If another BME280-based temperature sensor that supports I2C communication and a different I2C address are used, please rewrite address_temp in `~/git/pirad/scripts/python/control_hv.py`. Note that the DAC for HV control is also controlled by I2C communication and uses address 0x60, so duplicate addresses cannot be used.

### HV control parameters
The HV voltage is controlled by inputting a reference signal to the LT3482, an HV generation IC. The reference voltage is generated by the MCP4726, a 12-bit DAC chip with I2C communication, and is input to the LT3482 through a buffer. The control parameters of the DAC (maximum 12-bit = 4096) are adjusted according to the following formula to match the output voltage.
````
Channel = (HV+1.8821)/0.0213153
````
However, the output voltage and the voltage specified in the configuration file may change depending on the characteristics of mounted components such as resistors. Therefore, if you want to set more precise values, please calibrate and find the parameters, then change dac_const in `~/git/pirad/scripts/python/control_hv.py`. However, if an unexpected value is assigned, abnormal voltage may be supplied and cause the MPPC to malfunction, so please check the output voltage with a tester etc. before connecting.
