from machine import Pin
from utime import sleep

speaker = Pin(16, Pin.OUT)

print("Speaker turning on...")

while True:
    speaker.toggle()
    sleep(1)