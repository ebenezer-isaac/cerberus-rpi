from drivers.driver_lcd import lcd
from drivers.driver_fps import fps
lcd = lcddriver.lcd()
fps = fps()
lcd.clrscr()
lcd.println("Open FPS")
print 'Open FPS'
Initialize_FPS()
SetLED_FPS(True)
lcd.println("Press Finger")
print 'Press Finger'
WaitForFinger_FPS()
id = CapIdentify_FPS()
Terminate_FPS()
lcd.println("ID = "+str(id))
print 'ID = '+str(id)
