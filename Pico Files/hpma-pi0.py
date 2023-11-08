from __future__ import print_function
import serial, sys, time
import datetime, time
import os
import signal

LOGFILE = "logfile"

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

def exit_gracefully(a,b):
    print("set sleep")
    stopMeasurement()
    ser.close()
    os.path.isfile(LOGFILE) and os.access(LOGFILE, os.W_OK) and os.remove(LOGFILE)
    print("exit")
    exit(0)

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def sendSimpleCommand(cmd, description):
  for tried in range(5):
    try:
      ser.write(cmd)
      ret = ser.read(size=2)
    except Exception as ex:
      eprint(ex)
      exit(1)
    if len(ret) < 2:
      eprint("Error: only " + str(len(ret)) + " bytes received")
      continue

    if ret[0] != 0xa5 or ret[1] != 0xa5:
      print(description + ": ret should be 0xa5 0xa5, is", ret[0], ret[1])
    else:
      return
  eprint(description, "unsuccessful, exit")
  exit(1)


def startMeasurement():
  sendSimpleCommand(b'\x68\x01\x01\x96', "start measurement")

def stopMeasurement():
  sendSimpleCommand(b'\x68\x01\x02\x95', "stop measurement")

def stopAutoSend():
  sendSimpleCommand(b'\x68\x01\x20\x77', "stop auto send")

def readMeasurement():
  try:
      ser.write(b'\x68\x01\x04\x93')
      ret = ser.read(size=16)
  except:
      exit(1)
  
    if len(ret) < 8:
        eprint("Error: only " + len(ret) + " bytes received")
        exit(1)

    if ret[0] != 0x40 or ret[1] != 0xd or ret[2] != 0x4:
        eprint("header NOK\n0x40 0x05 0x04")
        for i in range(len(ret)):
            eprint(hex(ret[i]) + ' ',end='')
            eprint('')

  pm1 = int(ret[3]) * 256 + int(ret[4])
  pm25 = int(ret[5]) * 256 + int(ret[6])
  pm10 = int(ret[9]) * 256 + int(ret[10])
  output_string = '{0} {1} {2}'.format(pm1, pm25, pm10)

  return(output_string)


if __name__ == "__main__":
  print("resetting sensor...")
  ser.flushInput()
  stopMeasurement()
  time.sleep(2)

  stopAutoSend()
  print("starting measurement...")
  startMeasurement()
  stopAutoSend()

  for i in range(15): # throw away first measurements because of internal running average ove>
    output_string = readMeasurement()
    [pm1, pm25, pm10] = str(output_string).split(' ')
    print("PM1: {0} 2.5: {1} 10: {2}".format(pm1, pm25, pm10))
    time.sleep(1)

  print("starting logging.")
  while True:
    output_string = readMeasurement()
    [pm1, pm25, pm10] = str(output_string).split(' ')
    print("PM1: {0} 2.5: {1} 10: {2}".format(pm1, pm25, pm10))
#    logfilehandle = open(LOGFILE, "w",1)
#    logfilehandle.write(output_string)
#    logfilehandle.close()
    time.sleep(1)
