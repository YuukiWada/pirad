#!/usr/bin/env python
import spidev
import time

Vref = 5.0
#ch0 = [0x01,0x80,0x00]
#ch1 = [0x01,0xC0,0x00]

ch0 = [0b00000110, 0b00000000, 0b00000000]
#ch0 = [0b01100000, 0b00000000, 0b00000000]

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.max_speed_hz = 1000000

while True:
    adc = spi.xfer2(ch0)
    print(adc)
    #data = ((adc[1] & 0x0f) << 8) | adc[2]
    #print(data)
    time.sleep(0.02)

spi.close()
