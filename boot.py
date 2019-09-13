#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot sh /home/pi/cerberus-rpi/launcher.sh >/home/pi/bootlog/cronlog 2>&1' at the end of the file
import mysql.connector, subprocess, time, json, os
from drivers.lcd import LCD
from drivers.rtc import RTC
import datetime
import calendar
lcd = LCD()
rtc = RTC()
def print_time(ip):
        lcd.clrscr()
        lcd.println("System Ready")
        lcd.println(ip)
        lcd.println("Time :")
        x = rtc.getTime()
        t = time.time()
        print 'Printing time on LCD'
        print 'Press Ctrl + C to Abort'
	t = time.time()
	tx = time.time()
        while tx-t<120:
                y = rtc.getTime()
                if x!=y:
                        lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),4)
                        x = y
			tx = time.time()

def mod(num):
	if num<10:
		Mod = '0'+str(num)
	else:
		Mod = str(num)
	return Mod
lcd.clrscr()
lcd.println("System Ready")
lcd.println(" ")
lcd.println("Fetching IP")
ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
t = time.time()
while len(ip)<1:
	tx = time.time()
	if tx-t>=0.5:
		ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
print_time(ip)
