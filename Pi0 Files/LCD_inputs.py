import LCD1602
import time

lcd=LCD1602.LCD1602(16,2)

# Written with basic ideas for potential readouts
# From HCHO sensor
    # Get data of HCHO, humid, temp -> SS(hcho, humid, temp)
# From Honeywell
    # Get data from honeywell -> pm(pm1, pm25, pm 10)



try:
    while True:

        # COuld make these calls more common depending on what we find with the delay
        # Idea is that the value string updates in loop but these could move outside loop if 
        # we can continuosly update the string outside the loop
        # Redo below with correct calls for HCHO sensor
        SS = (1, 2, 3)

        # set the cursor to column 0, line 1
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("Formaldehyde")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f} ppb".format(SS[0]))

        #These rest values can be played with goal is to give time for user to read
        time.sleep(1.5)

        # HUmidity readout
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("Humidity")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f} %RH".format(SS[1]))
        time.sleep(1.5)

        # Temp readout
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("Temperature")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f} °C".format(SS[2]))
        time.sleep(1.5)


        #Redo below wih correct calls for PM Sensor
        pm = (1,2,3)

        # pm  1.0
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("PM 1.0")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f} ".format(pm[0]))
        time.sleep(1.5)

        # pm 2.5
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("PM 2.5")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f}".format(pm[1]))
        time.sleep(1.5)

        # pm 10
        lcd.setCursor(0, 0)
        # print category being read
        lcd.printout("PM 10")

        # set cursor to column 0, line 2
        lcd.setCursor(0, 1)
        # print category reading
        lcd.printout("{0:6.2f}".format(pm[2]))
        time.sleep(1.5)


except(KeyboardInterrupt):
    lcd.clear()
    del lcd
