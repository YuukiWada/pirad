#!/usr/bin/env python
import subprocess
import glob
import time
import sys

output_dir = sys.argv[1]
time.sleep(60)

while True:
    try:
        files = sorted(glob.glob("{}/20*.csv".format(output_dir)))
        if len(files)>1:
            for i in range(len(files)-1):
                subprocess.run("gzip {}".format(files[i]), shell=True)
        files = sorted(glob.glob("{}/hk_*.dat".format(output_dir)))
        if len(files)>1:
            for i in range(len(files)-1):
                subprocess.run("gzip {}".format(files[i]), shell=True)
        files = sorted(glob.glob("{}/gps_*.dat".format(output_dir)))
        if len(files)>1:
            for i in range(len(files)-1):
                subprocess.run("gzip {}".format(files[i]), shell=True)
        time.sleep(3600)
    except:
        print("Output directory is not found, aborting...")
        time.sleep(300)
