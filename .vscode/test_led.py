from machine import Pin
from utime import sleep

led = Pin("LED", Pin.OUT)

print("LED turning on...")

while True:
    led.toggle()
    sleep(1)