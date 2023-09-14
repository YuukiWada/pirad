#gcc -Wall -pthread -o daq daq.c -lpigpiod_if2 -lrt
gcc -Wall -pthread -o daq daq.c -lpigpio -lrt
#gcc -Wall -pthread -o daq daq.c -lpigpio -lrt -lwiringPi
