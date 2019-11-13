from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from functions import beep
from functions import blinkalt
beep(1)
blinkalt(1)
fps = FingerPi()
lcd = LCD()
lcd.clrscr()
lcd.println("Hello World")
fps.setLED(False)
fps.close()
