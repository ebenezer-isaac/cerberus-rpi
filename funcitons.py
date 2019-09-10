from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
import mysql.connector
import subprocess
import time
import os
fps = FingerPi()
lcd = LCD()
rtc = RTC()
host = "192.168.0.5"
user = "root"
password = "cerberus"
database = "cerberus"
def sync ():
    print 'Opening connection to database'
    myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
	cur = myconn.cursor()
    text = open("/templates/log.txt","rb") 
	logid = int(str(text.read()).strip())
	text.close()
    text = open("/templates/sync.txt","rb") 
	sync = int(str(text.read()).strip())
	text.close()
    try:
		sql="""SELECT logID, (select datedata.dateID from datedata,log where log.dateID=datedata.dateID) as date ,(select timedata.timeID from timedata,log where log.timeID=timedata.timeID)as time, comments FROM `log` where logTypeID=1 and logID>%s"""
		val = (logid)
        cur.execute(sql,val)
		result = cur.fetchall()
		for x in result:
			logid=x[0]
            date = x[1]
            date = x[2]
            comments = x[3]
            prn = comments[0]
            status = comments[1]
	except:
		myconn.rollback()
        
                    if status=='delete':
                os.remove("/templates/"+str(prn))
            elif status=='enroll':
                try:
                    sql="""select * from `fingerprints` where prn=%s"""
                    val = (prn)
                    cur.execute(sql,val)
                    fingerprints = cur.fetchall()
                    for y in result:
                        templateID=y[1]
                        template=y[2]
                        text = open(str(prn)+"-"+str(templateID)+".txt","wb") 
                        text.write(str(template)) 
                        text.close()
                except:
                    myconn.rollback()
    text = "templates/log.txt","wb") 
    text.write(str(logid)) 
    text.close()
    text = "templates/attendance.txt","r") 
    attandance = text.read() 
    text.close()
    line = 0
    while line<len(attendance):
        #insert attendance into database
        
def get_templates():
	print 'Opening connection...'
	id = 0
	myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
	cur = myconn.cursor()
	while id<=199:
		if fps.checkEnrolled(id):
			data = fps.getTemplate(id)
			text = open("./templates/template-id-"+str(id)+".txt","w") 
			text.write(str(data)) 
			text.close()
			print 'Template Fetched for id '+str(id)
			"""try:
				sql=insert into fingerprints values(%s, %s)
				val = (id,data)
				cur.execute(sql,val)
			except:
				myconn.rollback()"""
			print 'Template Uploaded for id '+str(id)
		id = id+1
	fps.deleteAll()
	myconn.close()
	print 'Connection closed'
	print 'Templates stored in templates folder successfully'

def identify():
	lcd.clrscr()
	lcd.println("Open FPS")
	print 'Open FPS'
	fps.setLED(True)
	lcd.println("Press Finger")
	print 'Press Finger'
	id = fps.identify()
	lcd.println("ID = "+str(id))
	print 'ID = '+str(id)

def print_enrolled():
	lcd.clrscr()
	lcd.println('Hello World')
	t = rtc.getTime()
	lcd.println(t)
	count = fps.countEnrolled()
	i = 0;
	print 'Total number of enrolled fingerprints = '+str(count)
	found=0
	while (found<count):
		if fps.checkEnrolled(i):
			print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
			found = found+1
		i=i+1
fps.open()
#print_enrolled()
identify()
#get_templates()
def time_increment():
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
			time_increment()

def set_templates():
	print 'Opening connection...'
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
