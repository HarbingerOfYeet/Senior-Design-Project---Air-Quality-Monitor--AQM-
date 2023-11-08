# Title: SFSART.py
# Description: code library defining communication via UART for HPMA115CO
# Author: Joe Pierzakowski
# BME 495 Senior Design
# Adapted for Raspberry Pi Pico using micropython from https://github.com/UnravelTEC/Raspi-Driver-HPM-series and code from Winston Ngo


from machine import UART, Pin
from utime import sleep

pm = UART(0, tx=Pin(16), rx=Pin(17))

def sendSimpleCommand(cmd, description):
    for tried in range(5):
        try:
            pm.write(cmd)
            num = pm.any()
            ret = pm.read()    # read 2 bytes
            print(num)
            print(ret)
        except Exception as error:
            print("An error occurred: ", error)
            return

        if ret is None:                                           
            print("Error: timeout")
        else:
            return
    print(description, "unsuccessful, exit")    

def startMeasurement():
    sendSimpleCommand(b'\x7e\x00\x00\x01\x00\xfe\x7e', "start measurement")

def stopMeasurement():
    sendSimpleCommand(b'\x7E\x00\x01\x00\xFE\x7E', "stop measurement")

def getDevice():
    sendSimpleCommand(b'\x7E\x00\xD0\x01\x06\x28\x7E', "get device info") 

def resetDevice():
    sendSimpleCommand(b'\x7E\x00\xD3\x00\x2C\x7E', "device reset")
    

def readMeasurement():
    try:
        pm.write(b'\x7E\x03\x01\x02\xF9\x7E')
        num = pm.any()
        ret = pm.read()    # read 8 bytes
        print(num)
        print(ret)
    except Exception as error:
        print("An error occurred: ", error)
        return
    
    if ret is None:
       print("Error: timeout")
    else:
       hcho = (256 * int(ret[5]) + int(ret[6])) / 5
        # = int(ret[5]) * 256 + int(ret[6])
    #    output_string = 'particulate_matter_ugpm3{{size="pm2.5",sensor="HPM"}} {0}\n'.format(pm25)
    #    output_string += 'particulate_matter_ugpm3{{size="pm10",sensor="HPM"}} {0}\n'.format(pm10)
    #    return(output_string)
    
    print("read measurment unsuccessful, exit")
    
print("resetting sensor...")
pm.flush()
resetDevice()
# stopMeasurement()
# getDevice()
sleep(2)

# print("Device info")
# getDevice()

# print("Starting measurement...")
# startMeasurement()

#for i in range(15): # throw away first measurements because of internal running average over 10s and fan speed up
    #output_string = readMeasurement()
    #print(output_string, end='')
    #sleep(1)
    
# stopMeasurement()

#pm.deinit()

#Error: object with buffer protocol required?
#
