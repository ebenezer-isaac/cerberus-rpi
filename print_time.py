import subprocess
import driver_lcd as lcddriver
import driver_rtc as rtcdriver
lcd = lcddriver.lcd()
rtc = rtcdriver.rtc()
sec = time.time()
while True:
	if sec-time.time()==1:
		time =rtc.getTime()
		ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
		lcd.clrscr()
		lcd.println("System Ready")
		lcd.println(ip)
		lcd.println(time)
		lcd.lcd_display_string(rtc.day,4)
		sec = time.time()


