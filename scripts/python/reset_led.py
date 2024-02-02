#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

while True:
  time.sleep(0.001)
  if GPIO.input(6)>0:
    time.sleep(0.02)
    GPIO.output(6, 0)
