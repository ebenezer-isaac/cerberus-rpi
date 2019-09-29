#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot sh /home/pi/cerberus-rpi/launcher.sh >/home/pi/bootlog/cronlog 2>&1' at the end of the file
import mysql.connector, subprocess, time, json, os
from drivers.lcd import LCD
from drivers.rtc import RTC
from drivers.fingerpi import FingerPi
import datetime
import calendar
import functions
import time
import RPi.GPIO as GPIO
lcd = LCD()
rtc = RTC()
fps = FingerPi()
def print_time():
	lcd.clrscr()
	lcd.println("Time :")
        x = rtc.getTime()
        t = time.time()
        print 'Printing time on LCD'
        print 'Press Ctrl + C to Abort'
	t = time.time()
	tx = time.time()
        while tx-t<5:
                y = rtc.getTime()
                if not x==y:
                        lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),3)
                        x = y
			tx = time.time()
def print_ip():
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
def get_prn(id):
    map = json.load(open("./docs/map.json"))
    prn = map[str(id)]
    return prn
def light_show():
	LedPin1 = 11
	LedPin2 = 12
        fade = 20
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(LedPin1, GPIO.OUT)
	GPIO.setup(LedPin2, GPIO.OUT)
	fps.setLED(True)
	while not fps.isPressFinger():
                GPIO.output(LedPin2,True)
                GPIO.output(LedPin1,False)
                time.sleep(0.5)
                GPIO.output(LedPin1,True)
                GPIO.output(LedPin2,False)
                time.sleep(0.5)
        GPIO.output(LedPin1,False)
        GPIO.output(LedPin2,False)
lcd.clrscr()
lcd.println("System Ready")
lcd.println("Initialize FPS")
fps.open()
#print_time()
while True:
    lcd.clrscr();
    lcd.println("Press Finger")
    id = fps.identify()
    if int(id)==200:
	lcd.clrscr()
        lcd.println("Finger not found")
	lcd.println("Light Show")
	beep(2)
	time.sleep(1)
	light_show()
    else:
        prn = get_prn(id)
        lcd.clrscr()
        lcd.println("PRN:"+str(prn))
        lcd.println("Wait 1 Second")
        time.sleep(1)
