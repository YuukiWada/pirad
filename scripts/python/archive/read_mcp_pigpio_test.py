#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pigpio

slct = 0
baud = 7800000
flag = 0
adch = 0

pi = pigpio.pi()
hndl = pi.spi_open(slct, baud, flag) # デバイスオープン
pi.set_mode(5, pigpio.OUTPUT)
pi.set_mode(6, pigpio.OUTPUT)

start_time = time.time()
while True:
  cmnd = ( 0b00011000 + adch ) << 2
  c, raw = pi.spi_xfer(hndl,[cmnd,0,0])
  data = ((raw[1] & 0b11111111) << 4) + ((raw[2] & 0b11110000) >> 4)
  #if data>0:
  #pi.write(5,1)
  #pi.write(5,0)
  print("{} {}".format(round(time.time()-start_time,6),data))
  #pi.write(6,1)
  #time.sleep(0.01)
  #pi.write(6,0)
    
    
