from machine import UART

# def __init__(self, id):
#         self._pm = UART(id, 9600)
        # self._pm.init(
        #     baudrate=9600,
        #     bits=8,
        #     parity=None,
        #     stop=1,
        #     tx=0,
        #     rx=1
        # )

pms = UART(0)

def flush(self):
    pms.flush()

def sendSimpleCommand(cmd, description):
    for tried in range(5):
        try:
            byt = pms.write(cmd)
            print(byt)
            ret = pms.read(2)    # read 2 bytes
            print(ret)
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
        pms.write(b'\x68\x01\x04\x93')
        ret = pms.read(8)    # read 8 bytes
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

if __name__ == "__main__":
    stopAutoSend()