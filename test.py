import LCD1602
import HPMA
from utime import sleep
from machine import Pin

lcd = LCD1602.LCD1602(16, 2)
led = Pin("LED", Pin.OUT)
pms = HPMA.HPMA(0)

# print("resetting sensor...")
# pms.flush()
# pms.stopMeasurement()
# sleep(2)

# pms.stopAutoSend()
# print("Starting measurement...")
# pms.startMeasurement()
# pms.stopAutoSend()

# for i in range(15): # throw away first measurements because of internal running average over 10s and fan speed up
#     output_string = pms.readMeasurement()
#     print(output_string, end='')
#     sleep(1)

# # output real data
# for i in range(15):
#     output_string = pms.readMeasurement()
#     print(output_string, end='')
#     sleep(1)

# print("powering down")
# pms.stopMeasurement()

try:
    while True:
        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)

        lcd.printout("Testing")

        lcd.setCursor(0, 1)

        lcd.printout("Hello World!")
        led.toggle()
        sleep(0.1)
except(KeyboardInterrupt):
    lcd.clear()
    del lcd
