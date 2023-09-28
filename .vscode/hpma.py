from machine import UART, Pin
from utime import sleep

pm = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

def sendSimpleCommand(cmd, description):
    for tried in range(5):
        try:
            pm.write(cmd)
            ret = pm.read(2)
        except:
            print("serial comm error")
            exit(1)

        if ret is None:                                           
            print("Error: timeout")
        elif len(ret) < 2:
            print(f"Error: only {len(ret)} bytes received")
        else:
            return
    print(description, "unsuccessful, exit")

def startMeasurement():
    sendSimpleCommand(b'\x68\x01\x01\x96', "start measurement")

def stopMeasurement():
    sendSimpleCommand(b'\x68\x01\x02\x95', "stop measurement")

def stopAutoSend():
    sendSimpleCommand(b'\x68\x01\x20\x77', "stop auto send")


def readMeasurement():
    try:
        pm.write(b'\x68\x01\x04\x93')
        ret = pm.read(8)
    except:
        exit(1)
    
    if ret is None:
        print("Error: timeout")
    else:
        pm25 = ret[3] * 256 + ret[4]
        pm10 = ret[5] * 256 + ret[6]
        output_string = 'particulate_matter_ugpm3{{size="pm2.5",sensor="HPM"}} {0}\n'.format(pm25)
        output_string += 'particulate_matter_ugpm3{{size="pm10",sensor="HPM"}} {0}\n'.format(pm10)
        return(output_string)
    
    print("Read Measurment unsuccessful, exit")


print("Starting measurement...")
startMeasurement()
sleep(2)
stopMeasurement()
print("Ended")