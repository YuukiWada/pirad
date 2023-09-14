#!/usr/bin/env ruby
require "pi_piper"

flag = false

PiPiper::Spi.begin do |spi|
  loop do
    first, center, last = spi.write [0b00000110, 0b00000000, 0b00000000]
    adc = (center&0b00001111) << 8 + last
    
    if adc>0 then
      puts "Event"
      `raspi-gpio set 5 dh & raspi-gpio set 5 dl`
    end
  end
end
