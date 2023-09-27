from machine import UART, Pin
from utime import sleep

sensor = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

def sendSimpleCommand(cmd, description):
  for tried in range(5):
    try:
      print("Writing", bytes(cmd, 'utf-8'))
      sensor.write(bytes(cmd, 'utf-8'))
      ret = sensor.read(2)
    except:
      print("serial comm error")
    if len(ret) < 2:
      print("Error: only " + str(len(ret)) + " bytes received")
      continue

    if ord(ret[0]) != 0xA5 or ord(ret[1]) != 0xA5:
      print(description + ": ret should be 0xA5 0xA5, is", hex(ord(ret[0])), hex(ord(ret[1])))
    else:
      return
  print(description, "unsuccessful, exit")

def startMeasurement():
  sendSimpleCommand("\x68\x01\x01\x96", "start measurement")

def stopMeasurement():
  sendSimpleCommand("\x68\x01\x02\x95", "stop measurement")

def stopAutoSend():
  sendSimpleCommand("\x68\x01\x20\x77", "stop auto send")


# def readMeasurement():
#   try:
#       sensor.write(bytes("\x68\x01\x04\x93", 'utf-8'))
#       ret = sensor.read(8)
#   except:
#       exit(1)
#   if len(ret) <8:
#     eprint("Error: only " + str(len(ret)) + " bytes received")
#     exit(1)

#   if ord(ret[0]) != 0x40 or ord(ret[1]) != 0x5 or ord(ret[2]) != 0x4:
#     eprint("header NOK\n0x40 0x05 0x04")
#     for i in range(len(ret)):
#       eprint(hex(ord(ret[i])) + ' ',end='')
#     eprint('')

#   pm25 = ord(ret[3]) * 256 + ord(ret[4])
#   pm10 = ord(ret[5]) * 256 + ord(ret[6])
#   output_string = 'particulate_matter_ugpm3{{size="pm2.5",sensor="HPM"}} {0}\n'.format(pm25)
#   output_string += 'particulate_matter_ugpm3{{size="pm10",sensor="HPM"}} {0}\n'.format(pm10)

#   return(output_string)

print("Starting measurement...")
startMeasurement()
sleep(2)
stopMeasurement()
print("Ended")