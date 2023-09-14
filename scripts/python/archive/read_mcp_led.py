#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pigpio
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

slct = 0
baud = 7800000
flag = 0
adch = 0

pi = pigpio.pi()
hndl = pi.spi_open(slct, baud, flag) # デバイスオープン

start_time = time.time()
while True:
  cmnd = ( 0b00011000 + adch ) << 2
  c, raw = pi.spi_xfer(hndl,[cmnd,0,0])
  data = ((raw[1] & 0b11111111) << 4) + ((raw[2] & 0b11110000) >> 4)
  #if data>0:
  GPIO.output(5, 1)
  GPIO.output(5, 0)
  print("{} {}".format(round(time.time()-start_time,6),data))
  GPIO.output(6, 1)
    #time.sleep(0.01)
    #GPIO.output(6, 0)
    
    
