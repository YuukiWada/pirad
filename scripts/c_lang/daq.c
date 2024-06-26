#include <pigpio.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>

void signal_handler(int signum)
{
  gpioTerminate();
  exit(1);
}

int main(int argc, char *argv[]){
  
  int threshold = atoi(argv[1]);
  int pin_reset = 5;
  int pin_led = 6;
  int spi_device = 0;
  int baud = 500000;
  int spi_flag = 0;
  const int data_length = 3;
  char conf[data_length];
  char adc[data_length];

  signal(SIGINT, signal_handler);
  //signal(SIGTERM, signal_handler);
  
  gpioInitialise();
  gpioSetMode(pin_reset, PI_OUTPUT);
  gpioSetMode(pin_led, PI_OUTPUT);
  int handle = spiOpen(spi_device, baud, spi_flag);

  conf[0] = 0b0000011;
  conf[1] = 0b0000000;
  conf[2] = 0b0000000;

  struct timeval time;
  gettimeofday(&time, NULL);
  double time_start = time.tv_sec+time.tv_usec/1000000.0;
  printf("%f\n",time_start);

  while (1){
    spiXfer(handle, conf, adc, data_length);
    int value = ((adc[1]&0x0f)<<8) | adc[2];
    if (value>threshold){
      gettimeofday(&time, NULL);
      double time_now = time.tv_sec+time.tv_usec/1000000.0;
      double delta_time = time_now-time_start;
      printf("%f, %i\n",delta_time,value);
      
      gpioWrite(pin_reset, 1);
      usleep(1);
      gpioWrite(pin_reset, 0);
      gpioWrite(pin_led, 1);
    }
  }
  return 0 ;
}
