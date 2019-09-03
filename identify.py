from driver_fps import *
from driver_lcd import *
import pickle
lcd = lcddriver.lcd()
lcd.lcd_display_string("Open FPS", 1)
Initialize_FPS()
SetLED_FPS(True)
lcd.lcd_display_string("Press Finger", 1)
WaitForFinger_FPS()
id = Identify_FPS()
Terminate_FPS()
print 'ID = '+str(id)