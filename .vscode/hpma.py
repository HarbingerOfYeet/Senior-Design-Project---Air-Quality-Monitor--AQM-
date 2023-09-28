from machine import UART
from utime import sleep

pm = UART(0)

def sendSimpleCommand(cmd, description):
    for tried in range(5):
        try:
            pm.write(cmd)
            ret = pm.read(2)
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
    except Exception as error:
        print("An error occurred: ", error)
        return
    
    if ret is None:
        print("Error: timeout")
    else:
        pm25 = int(ret[3]) * 256 + int(ret[4])
        pm10 = int(ret[5]) * 256 + int(ret[6])
        output_string = 'particulate_matter_ugpm3{{size="pm2.5",sensor="HPM"}} {0}\n'.format(pm25)
        output_string += 'particulate_matter_ugpm3{{size="pm10",sensor="HPM"}} {0}\n'.format(pm10)
        return(output_string)
    
    print("read measurment unsuccessful, exit")

if __name__ == "__main__":
    print("resetting sensor...")
    pm.flush()
    stopMeasurement()
    sleep(2)

    stopAutoSend()
    print("Starting measurement...")
    startMeasurement()
    stopAutoSend()

    for i in range(15): # throw away first measurements because of internal running average over 10s and fan speed up
        output_string = readMeasurement()
        print(output_string, end='')
        sleep(1)

    # output real data
    while True:
        output_string = readMeasurement()
        print(output_string, end='')
        sleep(1)