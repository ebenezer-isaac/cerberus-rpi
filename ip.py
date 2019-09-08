#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot sh /home/pi/cerberus-rpi/launcher.sh >/home/pi/bootlog/cronlog 2>&1' at the end of the file

import subprocess
import driver_lcd as lcddriver
import driver_rtc as rtcdriver
import time
def mod(num):
	if num<10:
		Mod = '0'+str(num)
	else:
		Mod = str(num)
	return Mod
lcd = lcddriver.lcd()
rtc = rtcdriver.rtc()
lcd.clrscr()
lcd.println("System Ready")
lcd.println(" ")
lcd.println("Fetching IP")
ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
lcd.println(str(len(ip)))
t = time.time()
while len(ip)<1:
	tx = time.time()
	if tx-t>=0.5:
		ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
lcd.clrscr()
lcd.println("IP:")
lcd.println(ip)
lcd.println("Boot Time :")
rtc.getTime()
lcd.lcd_display_string(mod(rtc.hour)+':'+mod(rtc.min)+':'+mod(rtc.sec)+' '+str(rtc.date)+'/'+mod(rtc.month)+'/'+mod(rtc.year),4)
