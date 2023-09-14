#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pigpio
import time

pi = pigpio.pi()
pi.set_mode(6, pigpio.OUTPUT)

while True:
  time.sleep(0.01)
  if pi.read(6)>0:
    time.sleep(0.01)
    pi.write(6,0)


    
    
