#!/usr/bin/env ruby
require "pi_piper"

pin = PiPiper::Pin.new(:pin => 27, :direction => :out)

loop do
  result = `ntpq -p`
  lines = result.split("\n")
  reach = lines[2].split("\s")[6].to_i
  if reach>=17 then
    pin.on
  else
    pin.off
  end
  sleep(10)
end
