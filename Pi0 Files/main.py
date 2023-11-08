# Author: Winston Ngo
# Date: Nov 8, 2023
#
# Main file to operate device. Measurements are read from both HPMA and SFA30 sensors.
# Measurements above a dangerous threshold will trigger vibration motors and display
# a message to the LCD to alert the user.
#
# Code for SFA3x and HPMA found online and adapted for this project.

import hpma_class
import signal
import RPi.GPIO as GPIO
from sys import exit
from ctypes import *
from time import sleep

# create hpma object
hpma = hpma_class.HPMA("/dev/ttyS0", 9600, 1)

# import sfa3x shared library
lib = CDLL("./raspberry-pi-i2c-sfa3x-master/libsfa3x.so");

# define signal handling
def signalHandler(sig, frame):
    print("set sleep")

    # stop measurement HPMA
    hpma.stopMeasurement()
    hpma.closeSerial()
    
    # stop measurement SFA30
    error = lib.sfa3x_stop_measurement()
    if (error):
        print("Error executing sfa3x_stop_measurement(): {0}".format(error))

    print("exit")
    exit(0)
    
signal.signal(signal.SIGINT, signalHandler)
signal.signal(signal.SIGTERM, signalHandler)

# main function
if __name__=="__main__":

    print("resetting sensors...")

    # reset HPMA
    hpma.flushInput()
    hpma.stopMeasurement()

    # reset sfa30
    lib.sensirion_i2c_hal_init()
    error = lib.sfa3x_device_reset()
    if (error):
        print("Error resetting SFA30: {0}\n".format(error))
        exit(1)

    sleep(2)

    print("starting measurement")
    
    # start HPMA measurement
    hpma.startMeasurement()
    hpma.stopAutoSend()

    # start SFA30 measurement
    error = lib.sfa3x_start_continuous_measurement()
    if (error):
        print("Error executing sfa3x_start_continuous_measurement(): {0}".format(error))
    
    # throw away first measurements because of internal running average over 10s and fan speed up
    for i in range(10):
        
        # read measurement from SFA30
        hcho = c_float()
        humid = c_float()
        temp = c_float()

        error = lib.sfa3x_read_measured_values(byref(hcho), byref(humid), byref(temp))

        if (error):
            print("Error executing sfa3x_read_measured_values(): {0}".format(error))
        else:
            print("Formaldehyde concentration: {0:6.2f} ppb".format(hcho.value))
            print("Relative humidity: {0:6.2f} %RH".format(humid.value))
            print("Temperature: {0:6.2f} °C".format(temp.value))

        # read measurement from HPMA
        outStr = hpma.readMeasurement()
        [pm1, pm25, pm10] = str(outStr).split(' ')
        print("PM1: {0}\nPM2.5: {1}\nPM10: {2}\n".format(pm1, pm25, pm10))
        sleep(1)

    time = 0
    print("starting logging")
    with open('logfile.csv', 'w') as f:

        # write the file header
        f.write("Time (s),PM2.5 (ug/m3),PM10 (ug/m3),HCHO (ppb)\n")
        
        # read measurement loop
        while True:
        
            # read measurement from SFA30
            hcho = c_float()
            humid = c_float()
            temp = c_float()
    
            error = lib.sfa3x_read_measured_values(byref(hcho), byref(humid), byref(temp))
    
            if (error):
                print("Error executing sfa3x_read_measured_values(): {0}".format(error))
            else:
                print("Formaldehyde concentration: {0:6.2f} ppb".format(hcho.value))
                print("Relative humidity: {0:6.2f} %RH".format(humid.value))
                print("Temperature: {0:6.2f} °C".format(temp.value))

            # read measurement from HPMA
            outStr = hpma.readMeasurement()
            [pm1, pm25, pm10] = str(outStr).split(' ')
            print("PM1: {0}\nPM2.5: {1}\nPM10: {2}\n".format(pm1, pm25, pm10))
            
            # write data to logfile.csv
            f.write("{0},{1},{2},{3:.2f}\n".format(time, pm25, pm10, hcho.value)) 

            time = time + 1
            sleep(1)
