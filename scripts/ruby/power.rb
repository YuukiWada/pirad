#!/usr/bin/env ruby
require "pi_piper"

switch = PiPiper::Pin.new(:pin => 21, :direction => :in)
led = PiPiper::Pin.new(:pin => 22, :direction => :out)

led.on

loop do
  switch.read
  if switch.on? then
    sleep(2.0)
    if switch.on? then
      led.off
      `sudo shutdown -h now`
    end
  end
  sleep(5.0)
end
