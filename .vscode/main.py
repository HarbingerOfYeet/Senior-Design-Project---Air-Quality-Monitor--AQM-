from machine import Pin
from utime import sleep

speaker = Pin(16, Pin.OUT)
led = Pin("LED", Pin.OUT)

print("Speaker turning on...")

while True:
    speaker.toggle()
    #led.toggle()
    #sleep(0.5)
    #speaker.low()