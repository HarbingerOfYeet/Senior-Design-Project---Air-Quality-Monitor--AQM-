# Title: HPMA.py
# Description: driver defining communication via UART for HPMA115CO
# Author: Winston Ngo
# BME 495 Senior Design
# Adapted for Raspberry Pi Pico using micropython from https://github.com/UnravelTEC/Raspi-Driver-HPM-series

from machine import UART

class HPMA:
    def __init__(self, id):
        self._pm = UART(id)

    def flush(self):
        self._pm.flush()

    def sendSimpleCommand(self, cmd, description):
        for tried in range(5):
            try:
                self._pm.write(cmd)
                ret = self._pm.read(2)    # read 2 bytes
            except Exception as error:
                print("An error occurred: ", error)
                return

            if ret is None:                                           
                print("Error: timeout")
            elif len(ret) < 2:
                print(f"Error: only {len(ret)} bytes received")
            else:
                return
        print(description, "unsuccessful, exit")

    def startMeasurement(self):
        self.sendSimpleCommand(b'\x68\x01\x01\x96', "start measurement")

    def stopMeasurement(self):
        self.sendSimpleCommand(b'\x68\x01\x02\x95', "stop measurement")

    def stopAutoSend(self):
        self.sendSimpleCommand(b'\x68\x01\x20\x77', "stop auto send")

    def readMeasurement(self):
        try:
            self._pm.write(b'\x68\x01\x04\x93')
            ret = self._pm.read(8)    # read 8 bytes
        except Exception as error:
            print("An error occurred: ", error)
            return
        
        if ret is None:
            print("Error: timeout")
        else:
            pm25 = int(ret[3]) * 256 + int(ret[4])
            pm10 = int(ret[5]) * 256 + int(ret[6])
            output_string = '{0} {1}'.format(pm25, pm10)
            return(output_string)
        
        print("read measurment unsuccessful, exit")