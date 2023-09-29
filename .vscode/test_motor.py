from machine import Pin
from utime import sleep

m1 = Pin(20, Pin.OUT)
m2 = Pin(16, Pin.OUT)
led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    if led.value() == 1:
        m1.high()
        m2.low()
    else:
        m1.low()
        m2.high()
    sleep(3)