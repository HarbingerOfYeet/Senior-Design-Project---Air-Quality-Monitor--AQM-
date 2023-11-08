# HPMA
# Author: Winston Ngo
# Date: Nov 8, 2023
#
# Class representing a HPMA sensor object
# Code adapted from github.com/UnravelTEC/Raspi-Driver-HPM-series

import serial
from sys import exit

class HPMA:
    def __init__(self, pt, br, to):
        self._ser = serial.Serial(port=pt, baudrate=br, timeout=to)

    def flushInput(self):
        self._ser.flushInput()

    def closeSerial(self):
        self._ser.close()

    def sendSimpleCommand(self, cmd, description):
      for tried in range(5):
        try:
          self._ser.write(cmd)
          ret = self._ser.read(size=2)
        except:
          print("serial comm error")
          exit(1)
        if len(ret) < 2:
          print("Error: only " + str(len(ret)) + " bytes received")
          continue

        if ret[0] != 0xa5 or ret[1] != 0xa5:
          print(description + ": ret should be 0xa5 0xa5, is", ret[0], ret[1])
        else:
          return
      print(description, "unsuccessful, exit")
      exit(1)

    def startMeasurement(self):
      self.sendSimpleCommand(b'\x68\x01\x01\x96', "start measurement")

    def stopMeasurement(self):
        self.sendSimpleCommand(b'\x68\x01\x02\x95', "stop measurement")

    def stopAutoSend(self):
      self.sendSimpleCommand(b'\x68\x01\x20\x77', "stop auto send")

    def readMeasurement(self):
      try:
          self._ser.write(b'\x68\x01\x04\x93')
          ret = self._ser.read(size=16)
          # print(ret)
      except:
          exit(1)
      if len(ret) <8:
        print("Error: only " + str(len(ret)) + " bytes received")
        exit(1)

      if ret[0] != 0x40 or ret[1] != 0xd or ret[2] != 0x4:
        print("header NOK\n0x40 0xd 0x04")
        for i in range(len(ret)):
          print(hex(ret[i]) + ' ',end='')
        print('')

      pm1 = int(ret[3]) * 256 + int(ret[4])
      pm25 = int(ret[5]) * 256 + int(ret[6])
      pm10 = int(ret[9]) * 256 + int(ret[10])
      output_string = '{0} {1} {2}'.format(pm1, pm25, pm10)

      return(output_string)
