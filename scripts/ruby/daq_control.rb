#!/usr/bin/env ruby
require "pi_piper"
require "time"
require "yaml"

input_dir = "/media/pi/data"
device_path = ["/dev/sda1", "/dev/sdb1", "/dev/sdc1", "/dev/sdd1"] 

def check_usb(input_dir, device_path, led)
  if !File.exist?(input_dir) then
    `sudo mkdir -p #{input_dir}`
    `sudo chown pi #{input_dir}`
  end
  loop do
    device_path.each do |device_path|
      if File.exist?(device_path) then
        result = `mountpoint #{input_dir}`
        if result.chomp=="#{input_dir} is not a mountpoint" then
          puts "#{input_dir} is not mounted."
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
    blink(led,2)
  end
end

def read_config(input_dir, led)
  input_file = "#{input_dir}/config.yaml"
  if !File.exist?(input_file) then
    blink(led,3)
    return false
  end
  data = open(input_file, "r") {|f| YAML.load(f)}

  if (data["hv"]!=nil)&&(data["threshold"]!=nil)&(data["compensation"]!=nil)&&(data["temp_const"]!=nil)&&(data["hv_limit"]!=nil) then
    return data
  else
    blink(led,3)
    return false
  end
end

def blink(led, num)
  num.times do
    led.on
    sleep(0.1)
    led.off
    sleep(0.25)
  end
  sleep(2.0)
end
     
switch = PiPiper::Pin.new(:pin => 20, :direction => :in)
led = PiPiper::Pin.new(:pin => 17, :direction => :out)
loop do
  time = Time.now
  time_past = time.strftime("%Y%m%d")
  switch.read
  if switch.on? then
    check_usb(input_dir, device_path, led)
    config = read_config(input_dir,led)
    if config!=false then
      hv = config["hv"]
      if config["compensation"]=="on" then
        compensation = 1
      else
        compensation = 0
      end
      const_temp = config["temp_const"]
      hv_limit = config["hv_limit"]
      threshold = config["threshold"]
      time = Time.now
      tstring = time.strftime("%Y%m%d_%H%M%S")
      puts "Observation starts"
      #`sudo python /home/pi/git/pirad/scripts/python/reset_led.py &`
      #`sudo python /home/pi/git/pirad/scripts/python/control_hv.py #{input_dir} #{hv} #{compensation} #{const_temp} #{hv_limit} &`
      #`/home/pi/git/pirad/scripts/c_lang/run_daq #{threshold} >> #{input_dir}/#{tstring}.csv &`
      spawn("sudo python /home/pi/git/pirad/scripts/python/reset_led.py &")
      spawn("sudo python /home/pi/git/pirad/scripts/python/control_hv.py #{input_dir} #{hv} #{compensation} #{const_temp} #{hv_limit} &")
      sleep(2.0)
      led.on
      spawn("/home/pi/git/pirad/scripts/c_lang/run_daq #{threshold} >> #{input_dir}/#{tstring}.csv &")
      loop do
        time=Time.now
        time_now=time.strftime("%Y%m%d")
        switch.read
        if switch.off? then
          `pkill -f reset_led`
          `pkill -f run_daq`
          `pkill -f hv_control`
          `sudo python /home/pi/git/pirad/scripts/python/stop_hv.py #{input_dir} #{compensation}`
          led.off
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
          blink(led,5)
          time_past=time_now
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
    end
  else
    led.off
    `sudo umount #{input_dir}`
    sleep(5.0)
  end
end
