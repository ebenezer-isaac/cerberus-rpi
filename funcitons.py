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
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    text = open("./templates/log.txt","rb")
    logid = int(str(text.read()).strip())
    text.close()
    sync = []
    with open('./templates/sync.txt', "rb") as fp:
        for i in fp.readlines():
    	    tmp = i.strip()
	    tmp = tmp.split(",")
	    try:
	        sync.append((tmp[0], tmp[1], tmp[2], tmp[3]))
            except:
	        pass
    try:
	sql="SELECT logID, (select datedata.date from datedata,log where log.dateID=datedata.dateID) as date ,(select timedata.time from timedata,log where log.timeID=timedata.timeID)as time, comments FROM `log` where logTypeID=1 and logID>"+str(logid)
	val = (logid)
        cur.execute(sql,val)
	result = cur.fetchall()
	for x in result:
	    logid=x[0]
            date = str(x[1]).replace("-","/")
            time = x[2]
            comments = x[3]
            log = str(date)+' '+str(time)+','+str(comments).replace(' ',',')+',db'
	    log = log.split(',')
	    sync.append((log[0],log[1],log[2],log[3]))
    except mysql.connector.Error as err:
        print(format(err))
    sync.sort()
    print sync
    for x in range(0,len(sync)):
	datetime = sync[x][0]
	template_name = sync[x][1]
    template_name = str(template_name).split('-')
    template_name = template_name[0]
    template_id = template_name[1]
	status = sync[x][2]
	source = sync[x][3]
	if source=='rpi':
        if status=='delete':
            if len(template_name[0])==16:
                sql="delete * from studentfingerprint where prn=%s and templateID=%s"
            else:
                sql="delete * from facultyfingerprint where facultyID=%s and templateID=%s"
            try:
				sql="delete * from studentfingerprint into fingerprints values %s, %s)"
				val = (template_name,template_id)
				cur.execute(sql,val)
                #insert into log for delete
                sql="insert into log values(1,,%s,%s)"
                val = ()
				cur.execute(sql,val)
			except:
				myconn.rollback()
        elif status=='enroll':
            if len(template_name[0])==16:
                sql="select template from studentfingerprint where prn=%s and templateID=%s"
            else:
                sql="select template from facultyfingerprint where facultyID=%s and templateID=%s"
            try:
                val = (template_name,template_id)
                cur.execute(sql,val)
                fingerprints = cur.fetchall()
                for y in result:
                    template=y[0]
                    text = open('/templates/'+str(template_name[0])+'-'+str(template_name[1])+'.txt','wb')
                    text.write(str(template))
                    text.close()
            except:
                myconn.rollback()
    elif source=='db':
        if status=='delete':
            os.remove('/templates/'+str(template_name)+'-'+str(template_id)+'.txt')
            #delete from fingerprint sensor
        elif status=='enroll':
            if len(template_name[0])==16:
                sql="select template from studentfingerprint values where prn=%s and templateID=%s"
            else:
                sql="select template from facultyfingerprint values where facultyID=%s and templateID=%s"
            try:
                val = (template_name,template_id)
                cur.execute(sql,val)
                fingerprints = cur.fetchall()
                for y in result:
                    template=y[0]
                    text = open('/templates/'+str(template_name[0])+'-'+str(template_name[1])+'.txt','wb')
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
def upload_template(template_name,template_id)
    template_name = int(template_name)
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
	cur = myconn.cursor()
    text = open(str(str('/templates/'+str(template_name[0])+'-'+str(template_name[1])+'.txt','rb') 
	template_data = text.read() 
	text.close()
    template_name = str(template_name).split('-')
    if len(template_name[0])==16:
        sql="insert into studentfingerprint values(%s, %s, %s)"
    else:
        sql="insert into studentfingerprint values(%s, %s, %s)"
    try:
        val = (template_name[0], template_name[1], template_data)
        cur.execute(sql,val)
    except mysql.connector.Error as err:
        print(format(err))
       
def get_templates():
	print 'Opening connection...'
	id = 0
	myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
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
sync()
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
	myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
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
