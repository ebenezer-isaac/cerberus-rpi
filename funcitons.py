from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
import mysql.connector
import subprocess
import time
fps = FingerPi()
lcd = LCD()
rtc = RTC()
"""
def get_templates():
	print 'Opening connection...'
	fps.open()
	id = 0
	myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
	cur = myconn.cursor()
	while id<=199:
		if CheckEnrolled_FPS(id):
			data = fps.getTemplate(id)
			text = open("./templates/template-id-"+str(id)+".txt","w") 
			text.write(str(data)) 
			text.close()
			print 'Template Fetched for id '+str(id)
			try:
				sql=insert into fingerprints values(%s, %s)
				val = (id,data)
				cur.execute(sql,val)
			except:
				myconn.rollback()
			print 'Template Uploaded for id '+str(id)
		id = id+1
	fps.deleteAll()
	fps.close()
	print 'Connection closed'
	print 'Templates stored in templates folder successfully'

def identify():
	lcd.clrscr()
	lcd.println("Open FPS")
	print 'Open FPS'
	fps.open()
	fps.setLED(True)
	lcd.println("Press Finger")
	print 'Press Finger'
	fps.identify_FPS()
	fps.close()
	lcd.println("ID = "+str(id))
	print 'ID = '+str(id)
"""
def print_enrolled():
	fps.open()
	count = fps.countEnrolled()
	i = 0;
	print 'Total number of enrolled fingerprints = '+str(count)
	found=0
	while (found<count):
		if fps.checkEnrolled(i):
			print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
			found = found+1
		i=i+1
	fps.close()
print_enrolled()
"""def increment():
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

def print_time():
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
def testing():
	id = 82
	print 'Opening connection... FPS'
	Initialize_FPS()
	print 'Counting Fingerprints : '
	count = CountEnrolled_FPS()
	i = 0;
	print 'Total number of enrolled fingerprints = '+str(count)
	found=1
	while (found<=count):
		if CheckEnrolled_FPS(i):
			print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
			found = found+1
		i=i+1
	print 'Fetching template for id '+str(id)
	t = time.time()
	data = GetTemplate_FPS(id)
	tx_time = time.time() - t
	print 'Template Fetched'
	print 'Time to transmit:', tx_time
	t = time.time()
	text = open("template.txt","rb") 
	template = text.read() 
	text.close()
	tx_time = time.time() - t
	print 'Template written to .txt file successfully'
	print 'Time write to text file:', tx_time
	t = time.time()
	DeleteId_FPS(id)
	tx_time = time.time() - t
	print 'Fingerprint has been deleted from scanner'
	print 'Time to delete fingerprint:', tx_time
	count = CountEnrolled_FPS()
	i = 0;
	print 'Counting Fingerprints : '
	print 'Total number of enrolled fingerprints = '+str(count)
	found=1
	while (found<=count):
	        if CheckEnrolled_FPS(i):
	                print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
	                found = found+1
	        i=i+1
	t = time.time()
	myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
	cur = myconn.cursor()
	print 'mysql connection established'
	try:
		sql="insert into fingerprints values(%s, %s)"
		val = (2017033800104472,template)
		cur.execute(sql,val)
	except:
		myconn.rollback()
	tx_time = time.time() - t
	print 'template uploaded to the database file'
	print 'Time to upload template:', tx_time
	t = time.time()
	try:
		cur.execute("select * from fingerprints where prn=2017033800104472")
		result = cur.fetchall()
		for x in result:
			data=x[1];
		tx_time = time.time() - t
		print 'template fetched from database'
		print 'Time to download:', tx_time
	except:
		myconn.rollback()
	myconn.close()
	print 'Database connection closed'
	t = time.time()
	text = open("dbtemp.txt","wb") 
	text.write(str(data)) 
	text.close()
	print 'data has been written to text file'
	print 'Time to write the template:', tx_time
	t = time.time()
	response = SetTemplate_FPS(id,str(data))
	tx_time = time.time() - t
	print 'Template sent to fps'
	print 'Time to set the template:', tx_time
	print 'setTemplate result = '+str(response[0]['ACK'])
	count = CountEnrolled_FPS()
	i = 0;
	print 'Counting Fingerprints : '
	print 'Total number of enrolled fingerprints = '+str(count)
	found=1
	while (found<=count):
		if CheckEnrolled_FPS(i):
			print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
			found = found+1
		i=i+1
	Terminate_FPS()
	print 'Connection closed'

def set_templates():
	print 'Opening connection...'
	Initialize_FPS()
	myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
	cur = myconn.cursor()
	DeleteAll_FPS()
	try:
		cur.execute("select * from fingerprints")
		result = cur.fetchall()
		for x in result:
			id=x[0]
			data = x[1]
			print id
			print 'Template Fetched for id '+str(id)
			text = open("./templates/template-id-"+str(id)+".txt","w") 
			text.write(str(data)) 
			text.close()
			print 'Template Written for id '+str(id)
			response = SetTemplate_FPS(id,str(data));
			print response
	except mysql.connector.Error as err:
		print("Something went wrong: {}".format(err))
	Terminate_FPS()
	print 'Connection closed'
	print 'Templates stored in templates folder successfully'
"""
