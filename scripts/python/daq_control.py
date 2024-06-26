#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time
import yaml
import os

input_dir = "/media/pi/pirad-data"
device_path = ["/dev/sda1", "/dev/sdb1", "/dev/sdc1", "/dev/sdd1"] 

def check_usb(input_dir, device_paths, led, switch):
    if not os.path.exists(input_dir):
        subprocess.run(["sudo", "mkdir", "-p", input_dir])
        subprocess.run(["sudo", "chown", "pi:pi", input_dir])

    while True:
        for device_path in device_paths:
            if os.path.exists(device_path):
                result = subprocess.run("mountpoint {}".format(input_dir), shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8")
                if result.stdout.strip() == "{} is not a mountpoint".format(input_dir):
                    print("{} is not mounted.".format(input_dir))
                    subprocess.run(["sudo", "umount", device_path])
                    time.sleep(2.0)
                    subprocess.run(["sudo", "mount", device_path, input_dir])
                    time.sleep(2.0)

                result = subprocess.run("mountpoint {}".format(input_dir), shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8")
                if result.stdout.strip() != "{} is not a mountpoint".format(input_dir):
                    print("{} is mounted.".format(device_path))
                    return True
            else:
                print("{} is not inserted.".format(device_path))
        
        blink(led, 2)
        time.sleep(2)
        if not GPIO.input(switch):
            return False

def read_config(input_dir, led):
    input_file = os.path.join(input_dir, "config.yaml")
    if not os.path.exists(input_file):
        blink(led, 3)
        return False
    with open(input_file, "r") as f:
        data = yaml.safe_load(f)

    if all(key in data for key in ["hv", "threshold", "compensation", "temp_const", "hv_limit"]):
        return data
    else:
        blink(led, 3)
        return False

def blink(led, num):
    for i in range(num):
        GPIO.output(led, 1)
        time.sleep(0.1)
        GPIO.output(led, 0)
        time.sleep(0.25)
    time.sleep(2)


switch = 20
led = 17

time.sleep(15)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

while True:
    current_time = time.strftime("%Y%m%d")
    #current_time = time.strftime("%Y%m%d-%H")
    
    if GPIO.input(switch):
        usb_res = check_usb(input_dir, device_path, led, switch)
        if usb_res:
            config = read_config(input_dir, led)

            if not config==False:
                hv = config["hv"]
                compensation = 1 if config["compensation"] else 0
                const_temp = config["temp_const"]
                hv_limit = config["hv_limit"]
                threshold = config["threshold"]
                
                tstring = time.strftime("%Y%m%d_%H%M%S")
                print("Observation starts")
                
                subprocess.Popen(["sudo", "python", "/home/pi/git/pirad/scripts/python/reset_led.py", "&"])
                subprocess.Popen(["sudo", "python", "/home/pi/git/pirad/scripts/python/control_hv.py", input_dir, str(hv), str(compensation), str(const_temp), str(hv_limit), "&"])
                subprocess.Popen(["sudo", "python", "/home/pi/git/pirad/scripts/python/compress.py", input_dir, "&"])
                subprocess.Popen("sudo python /home/pi/git/pirad/scripts/python/gps_logger.py {} &".format(input_dir), shell=True)
                time.sleep(2.0)
                GPIO.output(led,1)
                
                output_file = os.path.join(input_dir, f"{tstring}.csv")
                subprocess.run("sudo script -a -q -c '/home/pi/git/pirad/scripts/c_lang/run_daq {}' /dev/null | sudo tee -a {} >> /dev/null &".format(str(threshold), output_file), shell=True)
                
                while True:
                    time_now = time.strftime("%Y%m%d")
                    #time_now = time.strftime("%Y%m%d-%H")

                    if not GPIO.input(switch):
                        pid = subprocess.run("sudo pgrep -f run_daq", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f control_hv", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f reset_led", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f gps_logger", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f compress.py", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        subprocess.run(["sudo", "python", "/home/pi/git/pirad/scripts/python/stop_hv.py", input_dir, str(compensation)])
                        #subprocess.run(["pkill", "-f", "run_daq"])
                        #subprocess.run(["pkill", "-9", "-f", "run_daq"])
                        #subprocess.run(["pkill", "-9", "-f", "run_daq"])
                        #subprocess.run(["pkill", "-9", "-f", "control_hv"])
                        time.sleep(2.0)
                        #subprocess.run(["pkill", "-9", "-f", "reset_led"])
                        GPIO.output(led,0)
                        print("Observation stops")
                        time.sleep(5.0)
                        result = subprocess.getoutput(["sudo", "umount", input_dir])
                        if "busy" in result:
                            while True:
                                time.sleep(5.0)
                                result = subprocess.getoutput(["sudo", "umount", input_dir])
                                print("Busy")
                                if "busy" not in result:
                                    print("Not busy")
                                    break
                        blink(led, 5)
                        current_time = time_now
                        break
                    elif time_now != current_time:
                        print("File changed")
                        pid = subprocess.run("sudo pgrep -f run_daq", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f control_hv", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f reset_led", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f gps_logger", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        pid = subprocess.run("sudo pgrep -f compress.py", shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE ,encoding="utf-8").stdout
                        pid_command = pid.strip().split("\n")[0]
                        subprocess.run(["sudo", "kill", "-2", pid_command])
                        #subprocess.run(["pkill", "-9", "-f", "control_hv"])
                        #subprocess.run(["pkill", "-9", "-f", "reset_led"])
                        current_time = time_now
                        break
                    current_time = time_now
                    time.sleep(5.0)
    else:
        GPIO.output(led,0)
        subprocess.run(["sudo", "umount", input_dir])
        time.sleep(5.0)
