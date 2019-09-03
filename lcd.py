import subprocess
import driver_lcd as lcddriver
import driver_rtc as rtcdriver
lcd = lcddriver.lcd()
rtc = rtcdriver.rtc()
time =rtc.getTime()
ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
lcd.clrscr()
lcd.println("System Ready")
lcd.println(ip)
lcd.println(time)
lcd.println(rtc.day)
print time
print rtc.year
print rtc.month
print rtc.date
print rtc.hour
print rtc.min
print rtc.sec
print rtc.day
print ip

