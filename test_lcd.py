import LCD1602
from utime import sleep
from machine import Pin

lcd = LCD1602.LCD1602(16, 2)
led = Pin("LED", Pin.OUT)

try:
    while True:
        lcd.clear()
        led.toggle()
        if(led.value() == 0):
            lcd.setCursor(0, 0)
            lcd.printout("LED Off")
        else:
            lcd.setCursor(0, 0)
            lcd.printout("LED On")
        sleep(3)
except(KeyboardInterrupt):
    lcd.clear()
    del lcd