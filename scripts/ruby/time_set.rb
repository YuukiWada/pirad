#!/usr/bin/env ruby
require "json"
require "time"

ENV['TZ']="UTC"

#sleep(10)

loop do 
  gps_info=`gpspipe -w -n 5`
  gps_info.each_line do |line|
    puts line
    gps=JSON.parse(line)
    if gps["class"]=="TPV" then
      time_string_gps=gps["time"]
      if !time_string_gps.nil? then
        date=time_string_gps[0..9]
        hour=time_string_gps[11..18]
        gps_time="#{date} #{hour}"
        unixtime_gps=Time.parse(gps_time).to_i
        unixtime_rpi=Time.now.to_i
        if (unixtime_gps-unixtime_rpi).abs>30 then
          time_precise=Time.at(unixtime_gps)
          time_string=time_precise.strftime("%m/%d %H:%M:%S %Y")
          `date -s "#{time_string}"`
        end
      else
        puts "Time string is not good."
      end
      break
    end
  end
  sleep(60)
end
