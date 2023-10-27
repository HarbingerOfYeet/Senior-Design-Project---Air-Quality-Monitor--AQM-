import LCD1602
import HPMA
from utime import sleep
from machine import Pin

lcd = LCD1602.LCD1602(16, 2)
led = Pin("LED", Pin.OUT)
pms = HPMA.HPMA(0)
logfile = open("pm_data.csv", "w")

# boot up sensor
print("resetting sensor...")
pms.flush()
pms.stopMeasurement()
sleep(2)

pms.stopAutoSend()
print("Starting measurement...")
pms.startMeasurement()
pms.stopAutoSend()

for i in range(15): # throw away first measurements because of internal running average over 10s and fan speed up
    
    # read sensor data
    output_string = pms.readMeasurement()
    [pm25, pm10] = str(output_string).split(' ')

    # output sensor data to LCD
    lcd.setCursor(0, 0)
    lcd.printout('PM2.5:{0} 10:{1}'.format(pm25, pm10))

    lcd.setCursor(0, 1)
    lcd.printout("Measurement {0}".format(i))

    sleep(1)

# output real data
print("Starting data collection...")
lcd.clear()
sec = 0
try:
    while True:

        # read sensor data
        output_string = pms.readMeasurement()
        [pm25, pm10] = str(output_string).split(' ')

        # output sensor data to LCD
        lcd.setCursor(0, 0)
        lcd.printout('PM2.5:{0} 10:{1}'.format(pm25, pm10))

        # write measurement data to pm_data.csv
        # format: time,pm2.5,pm10
        logfile.write('{0},{1},{2}\n'.format(sec, pm25, pm10))
        
        sec = sec + 1
        sleep(1)

except KeyboardInterrupt as exception:
    logfile.close()
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("power down")
    lcd.clear()
    pms.stopMeasurement()