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
import LCD1602
import RPi.GPIO as GPIO
from sys import exit
from ctypes import *
from time import sleep

# threshold values for PM2.5, PM10, and HCHO to trigger warning message and vibration motors
WARNING_PM25 = 35
WARNING_PM10 = 150
WARNING_HCHO = 50

# create LCD object
lcd = LCD1602.LCD1602(16, 2)

# create hpma object
hpma = hpma_class.HPMA("/dev/ttyS0", 9600, 1)

# import sfa3x shared library using ctypes library
lib = CDLL("/home/pi/aqm/raspberry-pi-i2c-sfa3x-master/libsfa3x.so");

# setup GPIO pins for vibration motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

# define signal handling
def signalHandler(sig, frame):
    lcd.clear()
    GPIO.cleanup()
    
    # stop measurement HPMA
    hpma.stopMeasurement()
    hpma.closeSerial()
    
    # stop measurement SFA30
    error = lib.sfa3x_stop_measurement()
    if (error):
        print("Error executing sfa3x_stop_measurement(): {0}".format(error))
        exit(1)

    print("Exit successful")
    exit(0)
    
signal.signal(signal.SIGINT, signalHandler)
signal.signal(signal.SIGTERM, signalHandler)

# main function
if __name__=="__main__":

    # print("resetting sensors...")
    lcd.setCursor(0, 0)
    lcd.printout("Resetting")
    lcd.setCursor(0, 1)
    lcd.printout("Sensors...")
    sleep(2)
    lcd.clear()
    
    # reset HPMA
    hpma.flushInput()
    hpma.stopMeasurement()

    # reset sfa30
    lib.sensirion_i2c_hal_init()
    error = lib.sfa3x_device_reset()
    if (error):
        print("Error resetting SFA30: {0}\n".format(error))
        exit(1)

    # print("starting measurement in...")

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
        
        """
        if (error):
            print("Error executing sfa3x_read_measured_values(): {0}".format(error))
        else:
            print("Formaldehyde concentration: {0:6.2f} ppb".format(hcho.value))
            print("Relative humidity: {0:6.2f} %RH".format(humid.value))
            print("Temperature: {0:6.2f} °C".format(temp.value))
        """
        # read measurement from HPMA
        outStr = hpma.readMeasurement()
        [pm1, pm25, pm10] = str(outStr).split(' ')
        # print("PM1: {0}\nPM2.5: {1}\nPM10: {2}\n".format(pm1, pm25, pm10))
        
        sec = 10 - i
        lcd.setCursor(0, 0)
        lcd.printout("Starting in...")
        lcd.setCursor(0, 1)
        lcd.printout("{0}".format(sec))
        sleep(1)
        lcd.clear()

    # time = 0
    # print("starting logging")
    # with open('logfile.csv', 'w') as f:

    # write the file header
    # f.write("Time (s),PM2.5 (ug/m3),PM10 (ug/m3),HCHO (ppb)\n")
    
    # read measurement loop
    while True:

        lcd.setCursor(0, 0)

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
        
        # display warning message if PM2.5, PM10, or HCHO concentrations are above threshold concentrations
        if (int(pm25) > WARNING_PM25 or int(pm10) > WARNING_PM10):
            lcd.printout("WARNING!")
            lcd.setCursor(0, 1)
            lcd.printout("High PM levels")

            # buzz vibration motors for 8 seconds if the concentration of PM is rising (i.e. previous measurement is smaller)
            if (prevPM25 < int(pm25) and prevPM10 < int(pm10)):
                for i in range(8):
                    GPIO.output(29, True)
                    GPIO.output(31, True)
                    GPIO.output(33, True)
                    sleep(0.5)
                    GPIO.output(29, False)
                    GPIO.output(31, False)
                    GPIO.output(33, False)
                    sleep(0.5)
            lcd.clear()
            
        if (hcho.value > WARNING_HCHO):
            lcd.printout("WARNING!")
            lcd.setCursor(0, 1)
            lcd.printout("High HCHO levels")
            lcd.clear()
            # buzz vibration motors for 8 seconds if the concentration of HCHO is rising (i.e. previous measurement is smaller)
            if (prevHCHO < hcho.value):
                for i in range(8):
                    GPIO.output(29, True)
                    GPIO.output(31, True)
                    GPIO.output(33, True)
                    sleep(0.5)
                    GPIO.output(29, False)
                    GPIO.output(31, False)
                    GPIO.output(33, False)
                    sleep(0.5)
            lcd.clear()

        # cycle screen message every 5 seconds
        # 1: HCHO
        # 2: PM2.5 and PM10
        # 3: Temp and Humidity
        lcd.printout("HCHO:")
        lcd.setCursor(0, 1)
        lcd.printout("{0:.2f} ppb".format(hcho.value))
        sleep(4)
        lcd.clear()

        lcd.setCursor(0, 0)
        lcd.printout("PM2.5: {0} ug/m3".format(pm25))
        lcd.setCursor(0, 1)
        lcd.printout("PM10: {0} ug/m3".format(pm10))
        sleep(4)
        lcd.clear()

        lcd.setCursor(0, 0)
        lcd.printout("Temp: {0:.2f} C".format(temp.value))
        lcd.setCursor(0, 1)
        lcd.printout("Hum: {0:.2f} %RH".format(humid.value))
        sleep(4)
        lcd.clear()

        prevHCHO = hcho.value
        prevPM25 = int(pm25)
        prevPM10 = int(pm10)

        # write data to logfile.csv
        # f.write("{0},{1},{2},{3:.2f}\n".format(time, pm25, pm10, hcho.value)) 
        # time = time + 5
