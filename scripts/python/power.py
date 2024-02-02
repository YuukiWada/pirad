#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.OUT)

GPIO.output(22, 1)

while True:
    switch = GPIO.input(21)
    if switch:
        time.sleep(2.0)
        switch = GPIO.input(21)
        if switch:
            GPIO.output(22,0)
            subprocess.run(["sudo", "shutdown", "-h", "now"])
    time.sleep(5)
