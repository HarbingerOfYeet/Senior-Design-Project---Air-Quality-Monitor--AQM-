import LCD1602
import time
from machine import Pin

lcd = LCD1602.LCD1602(16, 2)
led = Pin("LED", Pin.OUT)

try:
    while True:
        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)

        lcd.printout("Testing")

        lcd.setCursor(0, 1)

        lcd.printout("Hello World!")
        led.toggle()
        time.sleep(0.1)
except(KeyboardInterrupt):
    lcd.clear()
    del lcd
