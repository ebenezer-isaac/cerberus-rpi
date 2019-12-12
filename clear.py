from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from functions import *
beep(4)
fps = FingerPi()
lcd = LCD()
lcd.clrscr()
lcd.println("Hello World")
fps.setLED(False)
fps.close()
