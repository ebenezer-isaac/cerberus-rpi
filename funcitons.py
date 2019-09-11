import mysql.connector, subprocess, time, json, os
from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
import datetime
import calendar
fps = FingerPi()
lcd = LCD()
rtc = RTC()
host = "192.168.0.5"
user = "root"
password = "cerberus"
database = "cerberus"
labid = 1
def sync ():
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    text = open("./docs/log.txt","rb")
    logid = int(str(text.read()).strip())
    text.close()
    sync = []
    with open('./docs/sync.txt', "rb") as fp:
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
	tmp = str(sync[x][0]).split()
	date = tmp[0]
	time = tmp[1]
	dateid = get_dateId(date)
	timeid = get_timeId(time)
	template_name = sync[x][1]
        temp = str(template_name).split('-')
        user_id = temp[0]
        template_id = temp[1]
	status = sync[x][2]
	source = sync[x][3]
        if source=='rpi':
            if status=='delete':
                if len(user_id)==16:
                    sql="delete * from studentfingerprint where prn=%s and templateID=%s"
                else:
                    sql="delete * from facultyfingerprint where facultyID=%s and templateID=%s"
                try:
		    val = (user_id,template_id)
		    cur.execute(sql,val)
   	            sql="insert into log values(1,%s,%s,%s)"
		    val = (dateid,timeid,template_name+' delete')
 	   	    cur.execute(sql,val)
                except mysql.connector.Error as err:
                    print(format(err))
            elif status=='enroll':
                if len(user_id)==16:
                   sql="insert into studentfingerprint values(%s, %s, %s)"
                else:
                   sql="insert into facultyfingerprint values(%s, %s,%s)"
                text = open('/templates/'+str(template_name)+'.txt','rb')
                template = text.read()
                text.close()
                try:
                    val = (user_id,template_id,template)
                    cur.execute(sql,val)
   	            sql="insert into log values(1,%s,%s,%s)"
		    val = (dateid,timeid,template_name+' enroll')
 	   	    cur.execute(sql,val)
                except mysql.connector.Error as err:
                    print(format(err))
        elif source=='db':
            if status=='delete':
                os.remove('/templates/'+str(template_name)+'.txt')
                map = json.load(open("./docs/map.json"))
		for fps_id in map:
		    if map[id]==str(template_name):
			fps.DeleteId(id)
			mps[id]='0'
	    elif status=='enroll':
                if len(user_id)==16:
                    sql="select template from studentfingerprint values where prn=%s and templateID=%s"
                else:
                    sql="select template from facultyfingerprint values where facultyID=%s and templateID=%s"
                try:
                    val = (user_id,template_id)
                    cur.execute(sql,val)
                    fingerprints = cur.fetchall()
                    for y in result:
                        template=y[0]
                        text = open('/templates/'+str(template_name)+'.txt','wb')
                        text.write(str(template))
                        text.close()
                except:
                    myconn.rollback()
    text = open("./docs/log.txt","wb")
    text.write(str(logid))
    text.close()
    text = open("./docs/attendance.txt","r")
    attandance = text.read()
    text.close()
    line = 0
    with open('./docs/attendance.txt', "rb") as fp:
        for i in fp.readlines():
    	    attendance = i.strip()
	    attendance = attendance.split(",")
	    dateid=get_dateId(attendance[0])
	    timeid=get_timeId(attendance[1])
	    slotid=get_timeId(attendance[1])
	    dayid = str(calendar.day_name[datetime.datetime(int(attendance[0][0:4]),int(attendance[0][5:7]),int(attendance[0][8:10])).weekday()]).lower()[0:3]
	    weekid = datetime.date(int(attendance[0][0:4]),int(attendance[0][5:7]),int(attendance[0][8:10])).isocalendar()[1]
	    scheduleid=get_scheduleid(slotid,weekid,dayid)
	    if len(attendance[2])==16:
 	        try:
   	            sql="insert into attendance values(%s,%s,%s,%s)"
		    val = (attendance[2],scheduleid,dateid,timeid)
 	   	    cur.execute(sql,val)
                except mysql.connector.Error as err:
                    print(format(err))
	    else:
 	        try:
   	            sql="UPDATE `timetable` SET `facultyID`=%s WHERE scheduleid=%s"
		    val = (attendance[2],scheduleid)
 	   	    cur.execute(sql,val)
                except mysql.connector.Error as err:
                    print(format(err))

def get_scheduleId(slotid,weekid,dayid):
    scheduleid = 0
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    try:
	sql="SELECT scheduleid from timetable where slotid=%s,labid=%s,weekid,dayid"
	val = (slotid,labid,weekid,dayid)
        cur.execute(sql,val)
	result = cur.fetchall()
	for x in result:
	    return x[0]
    except mysql.connector.Error as err:
        print(format(err))
def get_slotId(time):
    slotid = 0
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    try:
	sql="SELECT slotid from slot where endTime>%s and startTime>%s"
	val = (time,time)
        cur.execute(sql,val)
	result = cur.fetchall()
	for x in result:
	    return x[0]
    except mysql.connector.Error as err:
        print(format(err))
def get_timeId(time):
    timeid = 0
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    try:
	sql="SELECT timeID from timedata where time = %s"
	val = (time)
        cur.execute(sql,val)
	result = cur.fetchall()
	for x in result:
	    timeid=x[0]
	if timeid==0:
	    try:
   	        sql="insert into timedata values(%s)"
		val = (time)
 	   	cur.execute(sql,val)
		return get_timeId(time)
            except mysql.connector.Error as err:
                print(format(err))
    except mysql.connector.Error as err:
        print(format(err))
    return timeid
def get_dateId(time):
    dateid = 0
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    try:
	sql="SELECT dateID from datedata where date = %s"
	val = (date)
        cur.execute(sql,val)
	result = cur.fetchall()
	for x in result:
	    dateid=x[0]
	if dateid==0:
	    try:
   	        sql="insert into datedata values(%s)"
		val = (date)
 	   	cur.execute(sql,val)
		return get_dateId(date)
            except mysql.connector.Error as err:
                print(format(err))
    except mysql.connector.Error as err:
        print(format(err))
    return dateid

def upload_template(template_name,template_id):
    template_name = int(template_name)
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)  
    cur = myconn.cursor()
    text = open('/templates/'+str(template_name)+'-'+str(template_id)+'.txt','rb') 
    template_data = text.readlines() 
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
#fps.open()
#print_enrolled()
#identify()
#get_templates()
#sync()
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
"""
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
"""
