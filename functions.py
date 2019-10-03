import mysql.connector, subprocess, time, json, os, datetime, calendar, RPi.GPIO as GPIO
from drivers.fingerpi import FingerPi
#from drivers.lcd import LCD
#from drivers.rtc import RTC
fps = FingerPi()
#lcd = LCD()
#rtc = RTC()
host = "192.168.0.5"
user = "root"
password = "cerberus"
database = "cerberus"
labid = 1
def beep(sec):
        BuzzPin =36
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(BuzzPin, GPIO.OUT)
        count = 1
        while count<=sec:
                GPIO.output(BuzzPin,True)
                time.sleep(0.1)
                GPIO.output(BuzzPin,False)
                time.sleep(0.2)
                count = count+1
        GPIO.output(BuzzPin,False)
def sync_templates ():
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
def sync_attendance():
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
def sync_timetable():
    sql = "select slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID from timetable inner join slot on timetable.slotID = slot.slotID where timetable.labID=%s and timetable.dayID=%s and timetable.weekID=%s"
def get_scheduleId(slotid,weekid,dayid):
    scheduleid = 0
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

def print_enrolled():
    lcd.clrscr()
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

def print_time():
	ip = str(subprocess.check_output("hostname -I", shell=True)).strip()
	lcd.clrscr()
	lcd.println("System Ready")
	lcd.println(ip)
	lcd.println("Time :")
	x = rtc.getTime()
	t = time.time()
	print 'Printing time on LCD'
	print 'Press Ctrl + C to Abort'
	while True:
		y = rtc.getTime()
		if x!=y:
			lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),4)
			x = y
def set_template(template_name,fps_id):
    text = open("./templates/"+str(template_name)+".txt","rb") 
    template_data = text.readlines() 
    text.close()
    response = fps.setTemplate(id,str(template_data));
    print response
    print 'Templates written to fps successfully'
