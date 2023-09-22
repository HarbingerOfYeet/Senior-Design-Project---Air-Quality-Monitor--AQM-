from machine import Pin
from utime import sleep

motor = Pin(16, Pin.OUT)

while True:
    motor.high()