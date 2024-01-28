#! /usr/bin/env python
# -*- coding: utf-8 -*-
from bme280 import bme280
from bme280 import bme280_i2c
import datetime
import smbus
import sys
import time
import RPi.GPIO as GPIO

output_dir = sys.argv[1]
hv_ref = float(sys.argv[2])
comp_sw = int(sys.argv[3])
const_temp = float(sys.argv[4])
hv_limit = float(sys.argv[5])

interval = 1800 # sec
interval_measure = 300 # sec
temp_base = 25.0

i2c = smbus.SMBus(1)
address_temp = 0x76
address_dac = 0x60
dac_const = [1.8821,0.0213153]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

hv = 0
hv_previous = 0

if comp_sw==1:
  bme280_i2c.set_default_i2c_address(address_temp)
  bme280_i2c.set_default_bus(1)
  bme280.setup()
  max_count = round(interval/interval_measure)
  count = max_count-1

  while True:
    try:
      data_all = bme280.read_all()
      temp = round(data_all.temperature,2)
      humid = round(data_all.humidity,2)
      press = round(data_all.pressure,2)
      hv = hv_ref + (temp-temp_base)*const_temp
      if (hv>hv_limit) or (hv<0):
        hv = 0
    except:
      temp = False
      humid = False
      press = False
      hv = 0
    ut = round(time.time())
    dt = datetime.datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")
    output_file = "{}/hk_{}.dat".format(output_dir,datetime.datetime.fromtimestamp(ut).strftime("%Y%m%d"))
    if (count==max_count-1) or (hv==0):
      with open(output_file, "a") as f:
        f.write("{}, {}, {}, {}, {}, {}\n".format(ut,dt,hv,temp,humid,press))
        print("{}, {}, {}, {}, {}, {}".format(ut,dt,hv,temp,humid,press))
      hv_command = round((hv+dac_const[0])/dac_const[1])
      if hv_command<0:
        hv_command = 0
      command = [(hv_command&0xff0)>>4, (hv_command&0x00f)<<4]
      i2c.write_i2c_block_data(address_dac, 0x40, command)
      print("HV changed.")
      if hv>0:
        GPIO.output(13, 1)
      else:
        GPIO.output(13, 0)
      count = 0
      hv_previous = hv
      time.sleep(interval_measure)
    else:
      with open(output_file, "a") as f:
        f.write("{}, {}, {}, {}, {}, {}\n".format(ut,dt,hv_previous,temp,humid,press))
        print("{}, {}, {}, {}, {}, {}".format(ut,dt,hv_previous,temp,humid,press))
      count+=1
      time.sleep(interval_measure)
      
else:
  max_count = round(interval/interval_measure)
  count = max_count-1

  while True:
    ut = round(time.time())
    dt = datetime.datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")
    hv = hv_ref
    if (hv>hv_limit) or (hv<0):
      hv = 0
    output_file = "{}/hk_{}.dat".format(output_dir,datetime.datetime.fromtimestamp(ut).strftime("%Y%m%d"))
    with open(output_file, "a") as f:
      f.write("{}, {}, {}\n".format(ut,dt,hv))
      print("{}, {}, {}".format(ut,dt,hv))
    if (count==max_count-1) or (hv==0):
      hv_command = round((hv+dac_const[0])/dac_const[1])
      if hv_command<0:
        hv_command = 0
      command = [(hv_command&0xff0)>>4, (hv_command&0x00f)<<4]
      i2c.write_i2c_block_data(address_dac, 0x40, command)
      print("HV changed.")
      if hv>0:
        GPIO.output(13, 1)
      else:
        GPIO.output(13, 0)
      count = 0
      time.sleep(interval_measure)
    else:
      count += 1
      time.sleep(interval_measure)
      
