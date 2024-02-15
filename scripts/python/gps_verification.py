#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

while True:
    result = subprocess.run("chronyc sources -v", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8")
    lines = result.stdout.split("\n")
    for line in lines:
        parse = line.split()
        if len(parse)>1:
            if parse[1] == "GPS":
                if parse[0] == "#*":
                    print("GPS synchronized")
                    GPIO.output(27,1)
                else:
                    print("GPS not synchronized")
                    GPIO.output(27,0)
    time.sleep(30)
