from machine import Pin
from utime import sleep

m1 = Pin(20, Pin.OUT)
m2 = Pin(21, Pin.OUT)

try:
    while True:
        m1.high()
        m2.high()
except:
    m1.low()
    m2.low()