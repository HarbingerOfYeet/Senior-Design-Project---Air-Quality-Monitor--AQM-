import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

# blink motor
try:
    for i in range(20):
        GPIO.output(29, True)
        GPIO.output(31, True)
        GPIO.output(33, True)
        time.sleep(1)
        #GPIO.output(29, False)
        #GPIO.output(31, False)
        #GPIO.output(33, False)
        #time.sleep(0.5)
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
