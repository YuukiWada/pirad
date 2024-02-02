#!/usr/bin/env ruby
require "json"
require "time"

ENV['TZ']="UTC"
output_dir = ARGV[0]
output_file = "#{output_dir}/gps_#{Time.now.strftime("%Y%m%d")}.dat"

loop do 
  gps_info=`gpspipe -w -n 10`
  File.open(output_file, "a") do |input|
    input.puts(gps_info)
  end
  sleep(300)
end
