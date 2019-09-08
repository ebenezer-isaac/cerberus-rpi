#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot sh /home/pi/cerberus-rpi/launcher.sh >/home/pi/bootlog/cronlog 2>&1' at the end of the file

from drivers.lcd import LCD
from drivers.rtc import RTC
import subprocess
import time
lcd = LCD()
rtc = RTC()
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
lcd.println(str(rtc.getTime()),4)
