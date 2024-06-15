#! /usr/bin/env python
# -*- coding: utf-8 -*-
from gps3 import gps3
import datetime
import sys
import time

output_dir = sys.argv[1]

time.sleep(5)

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

while True:
    current_time = time.strftime("%Y%m%d")
    time_previous = ""
    output_file = "{}/gps_{}.dat".format(output_dir,current_time)
    with open(output_file, "a") as f:
        for new_data in gps_socket:
            time_now = time.strftime("%Y%m%d")
            if time_now != current_time:
                break
            if new_data:
                data_stream.unpack(new_data)
                if(data_stream.TPV['time'] == 'n/a'):
                    continue
                dlist = [data_stream.TPV['mode'],
                        data_stream.TPV['time'],
                        data_stream.TPV['lat'],
                        data_stream.TPV['lon'],
                        data_stream.TPV['alt'],
                        data_stream.TPV['speed'],
                        data_stream.TPV['epx'],
                        data_stream.TPV['epy']]
                if dlist[1][0:18] != time_previous:
                    f.write("{},{},{},{},{},{},{},{}\n".format(dlist[0],dlist[1],dlist[2],dlist[3],dlist[4],dlist[5],dlist[6],dlist[7]))
                    f.flush()
                time_previous = dlist[1][0:18]
            current_time = time_now
