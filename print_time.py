import subprocess
import driver_lcd as lcddriver
import driver_rtc as rtcdriver
import time
def increment():
	sec = rtc.sec
	min = rtc.min
	hour = rtc.hour
	sec=sec+1
	if sec>59:
		sec=0
		min=min+1
		if min>59:
			min=0
			hour=hour+1
			if hour>23:
				hour=0

	rtc.sec = sec
	rtc.min = min
	rtc.hour = hour
def mod(num):
	if num<10:
		Mod = '0'+str(num)
	else:
		Mod = str(num)
	return Mod
lcd = lcddriver.lcd()
rtc = rtcdriver.rtc()
ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
lcd.clrscr()
lcd.println("System Ready")
lcd.println(ip)
lcd.println("Time :")
rtc.getTime()
t = time.time()
print 'Printing time on LCD'
print 'Press Ctrl + C to Abort'
while True:
	tx = time.time()
	if tx-t>1:
		lcd.lcd_display_string(mod(rtc.hour)+':'+mod(rtc.min)+':'+mod(rtc.sec)+' '+str(rtc.date)+'/'+mod(rtc.month)+'/'+mod(rtc.year),4)
		t = time.time()
		increment()
