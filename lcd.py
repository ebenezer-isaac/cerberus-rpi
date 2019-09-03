import driver_lcd as lcddriver
import driver_rtc as rtcdriver
lcd = lcddriver.lcd()
rtc = rtcdriver.rtc()
time =rtc.getTime()
lcd.println("Hello world")
lcd.println("Ebenezer Isaac")
lcd.println(time)
print time
print rtc.year
print rtc.month
print rtc.date
print rtc.hour
print rtc.min
print rtc.sec
print rtc.day


