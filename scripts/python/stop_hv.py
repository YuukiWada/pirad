#! /usr/bin/env python
# -*- coding: utf-8 -*-
from bme280 import bme280
from bme280 import bme280_i2c
import smbus
import datetime
import sys
import time
import RPi.GPIO as GPIO

output_dir = sys.argv[1]
comp_sw = int(sys.argv[2])

i2c = smbus.SMBus(1)
address_temp = 0x76
address_dac = 0x60
dac_const = [1.8821,0.0213153]

hv = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

if comp_sw==1:
  try:
    bme280_i2c.set_default_i2c_address(address_temp)
    bme280_i2c.set_default_bus(1)
    bme280.setup()
    data_all = bme280.read_all()
    temp = round(data_all.temperature,2)
    humid = round(data_all.humidity,2)
    press = round(data_all.pressure,2)
    hv = 0
  except:
    hv = 0
  ut = round(time.time())
  dt = datetime.datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")
  output_file = "{}/hk_{}.dat".format(output_dir,datetime.datetime.fromtimestamp(ut).strftime("%Y%m%d"))
  with open(output_file, "a") as f:
    f.write("{}, {}, {}, {}, {}, {}\n".format(ut,dt,hv,temp,humid,press))
  i2c.write_i2c_block_data(address_dac, 0x40, [0,0])
  GPIO.output(13, 0)
      
else:
  ut = round(time.time())
  dt = datetime.datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")
  hv = 0
  output_file = "{}/hk_{}.dat".format(output_dir,datetime.datetime.fromtimestamp(ut).strftime("%Y%m%d"))
  with open(output_file, "a") as f:
    f.write("{}, {}, {}\n".format(ut,dt,hv))
  i2c.write_i2c_block_data(address_dac, 0x40, [0,0])
  GPIO.output(13, 0)
