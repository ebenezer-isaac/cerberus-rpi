from driver_fps import *
import driver_lcd as lcddriver
import pickle
lcd = lcddriver.lcd()
lcd.println("Open FPS")
print 'Open FPS'
Initialize_FPS()
SetLED_FPS(True)
lcd.println("Press Finger")
print 'Press Finger'
WaitForFinger_FPS()
id = Identify_FPS()
Terminate_FPS()
lcd.println("ID = "+str(id))
print 'ID = '+str(id)
