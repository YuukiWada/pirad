#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

while True:
    result = subprocess.run("ntpq -p", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8")
    lines = result.stdout.split("\n")
    print(lines[2].split())
    reach = int(lines[2].split()[6])

    if reach>=17:
        GPIO.output(27,1) 
    else:
        GPIO.output(27,0) 
    time.sleep(10)

