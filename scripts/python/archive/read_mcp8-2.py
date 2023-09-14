# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 08:48:17 2020

@author: Souichirou Kikuchi
"""

import spidev
from time import sleep

V_REF = 3.29476 # input Voltage
CHN = 0 # 接続チャンネル

spi = spidev.SpiDev()
spi.open(0, 0) # 0：SPI0、0：CE0
spi.max_speed_hz = 1000000 # 1MHz SPIのバージョンアップによりこの指定をしないと動かない

def get_voltage():
    dout = spi.xfer2([((0b1000+CHN)>>2)+0b100,((0b1000+CHN)&0b0011)<<6,0]) # Din(RasPi→MCP3208）を指定
    bit12 = ((dout[1]&0b1111) << 8) + dout[2] # Dout（MCP3208→RasPi）から12ビットを取り出す
    volts = round((bit12 * V_REF) / float(4095),4)  # 取得した値を電圧に変換する（12bitなので4095で割る）
    return volts # 電圧を返す

try:
    print('--- start program ---')
    while True:
        volts = get_voltage()
        if volts>0:
            print('volts= {:3.2f}'.format(volts))
        #sleep(1)

except KeyboardInterrupt:
    pass
finally:
    spi.close()
    print('--- stop program ---')
