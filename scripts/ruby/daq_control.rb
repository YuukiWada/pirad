#!/usr/bin/env ruby
require "pi_piper"
require "time"

input_dir = "/media/pi/data"
device_path = ["/dev/sda1", "/dev/sdb1", "/dev/sdc1", "/dev/sdd1"] 

def check_usb(input_dir, device_path)
  if !File.exist?(input_dir) then
    `sudo mkdir -p #{input_dir}`
  end
  loop do
    device_path.each do |device_path|
      if File.exist?(device_path) then
        result = `mountpoint #{input_dir}`
        if result.chomp=="#{input_dir} is not a mountpoint" then
          puts "/dev/sda1 is not mounted."
          `sudo umount #{device_path}`
          sleep(2.0)
          `sudo mount #{device_path} #{input_dir}`
          sleep(2.0)
        end
        
        result = `mountpoint #{input_dir}`
        if result.chomp!="#{input_dir} is not a mountpoint" then
          puts "#{device_path} is mounted."
          return 0
        end
      else
        puts "#{device_path} is not inserted."
      end
    end
    sleep(5.0)
  end
end


switch = PiPiper::Pin.new(:pin => 20, :direction => :in)
led = PiPiper::Pin.new(:pin => 17, :direction => :out)
loop do
  time = Time.now
  time_past = time.strftime("%Y%m%d")
  switch.read
  if switch.on? then
    check_usb(input_dir, device_path)
    time = Time.now
    tstring = time.strftime("%Y%m%d_%H%M%S")
    led.on
    puts "Observation starts"
    `sudo ruby /home/pi/git/pirad/scripts/run_daq #{threshold} >> #{input_dir}/#{tstring}.csv &`
    loop do
      time=Time.now
      time_now=time.strftime("%Y%m%d")
      switch.read
      if switch.off? then
        `pkill -f read_mcp`
        puts "Observation stops"
        sleep(5.0)
        result=`sudo umount #{input_dir} 2>&1`
        if result.include?("busy") then
          loop do
            sleep(5.0)
            result=`sudo umount #{input_dir} 2>&1`
            puts "Busy"
            if !result.include?("busy") then
              puts "Not busy"
              break
            end
          end
        end
        time_past=time_now
        led.off
        break
      elsif time_now!=time_past then
        puts "File changed"
        `pkill -f read_mcp`
        time_past=time_now
        break
      end
      time_past=time_now
      sleep(5.0)
    end
  else
    led.off
    `sudo umount #{input_dir}`
    sleep(5.0)
  end
end
