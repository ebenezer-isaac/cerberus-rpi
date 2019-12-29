from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from functions import *
setup()
fps = FingerPi()
lcd = LCD()
lcd.clrscr()
lcd.println("Hello World")
fps.open()
print 'FPS Light'
fps.setLED(True)
fps.setLED(False)
fps.close()
