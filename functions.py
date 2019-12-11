import mysql.connector, subprocess, time, json, os, datetime, calendar, RPi.GPIO as GPIO, threading
from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
fps = FingerPi()
lcd = LCD()
rtc = RTC()
host = "192.168.0.7"
user = "root"
password = "cerberus"
database = "cerberus"
labid = 1
BuzzPin =36
GreenPin = 26
RedPin = 18
MATRIX = [
[1,2,3,'A'],
[4,5,6,'B'],
[7,8,9,'C'],
['*',0,'#','D']
]
COL = [32,37,33,31]
ROW = [29,15,13,11]

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(BuzzPin, GPIO.OUT)
    GPIO.setup(GreenPin, GPIO.OUT)
    GPIO.setup(RedPin, GPIO.OUT)
    while not fps.open:
        fps.open()
    for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j],1)
    for i in range(4):
        GPIO.setup(ROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)
    beep(4);

def sleep(milsec):
    time.sleep(milsec/1000)

def getKeyPress():
    key = ''
    while key == '':
        for  j in range(4):
            GPIO.output(COL[j],0)
            for i in range(4):
                if GPIO.input(ROW[i])==0:
                    key = MATRIX[i][j]
                    while (GPIO.input(ROW[i])==0):
                        time.sleep(0.2)
                    return key
            GPIO.output(COL[j],1)

def println(text):
	lcd.println(text)
def printline(text,line):
	lcd.println(text,line)
def clrscr():
	lcd.clrscr()
def identify():
    fps.waitForFinger()
    id = fps.identify()
    if int(id)==200:
        clrscr()
        beep(2)
        return "Finger not found"
    else:
        return "Name : "+get_map_prn(id)

def enroll(id):
    response = False
    errFCount=0
    while errFCount<=2 and fps.enroll(id)[0]['Parameter']==0 and not fps.checkEnrolled(id):
	errCount=0
        while errCount<=2:
	    lcd.clrscr()
	    lcd.println('Enroll Started')
	    lcd.println("Press Finger")
	    fps.waitForFinger()
	    if fps.captureFinger(True):
                fps.enroll1()
	        lcd.clrscr()
	        lcd.println("Image Captured 1/3")
                lcd.println("Remove finger")
	        fps.waitForRemove()
	        lcd.clrscr()
		break
	    else:
	 	errCount= errCount+1
	        lcd.clrscr()
	 	lcd.println("Failed - 1st Image")
 	 	lcd.println("Dry/Wet/Dirty Finger")
                lcd.println("Please Try Again")
	 	lcd.println("Trial : "+str(errCount))
	    	sleep(1000)
	errCount=0
	while errCount<=2:
	    lcd.clrscr()
	    lcd.println("Press Finger Again")
	    fps.waitForFinger()
	    if fps.captureFinger(True):
                fps.enroll2()
	        lcd.clrscr()
	        lcd.println("Image Captured 2/3")
                lcd.println("Remove finger")
	        fps.waitForRemove()
	        lcd.clrscr()
	        break
	    else:
		errCount= errCount+1
	        lcd.clrscr()
		lcd.println("Failed - 2nd Image")
 		lcd.println("Dry/Wet/Dirty Finger")
                lcd.println("Please Try Again")
		lcd.println("Trial : "+str(errCount))
		sleep(1000)
	errCount=0
	while errCount<=2:
	    lcd.clrscr()
	    lcd.println("Press Finger Again")
	    fps.waitForFinger()
	    if fps.captureFinger(True):
                response = fps.enroll3()
		if response==0:
		    response = True
	        else:
		    errFCount=errFCount+1
		lcd.clrscr()
	        lcd.println("Image Captured 3/3")
                lcd.println("Remove finger")
	        fps.waitForRemove()
		errFCount=4
		break
	    else:
		errCount= errCount+1
	        lcd.clrscr()
		lcd.println("Failed - 3rd Image")
 		lcd.println("Dry/Wet/Dirty Finger")
                lcd.println("Please Try Again")
		lcd.println("Trial : "+str(errCount))
		sleep(1000)
        if response==False:
	    lcd.clrscr()
	    lcd.println("Enroll Failed")
 	    lcd.println("Press Finger Proprly")
            lcd.println("Please Try Again")
	    lcd.println("Trial : "+str(errFCount))
    fps.setLED(False)
    return response
def beep(sec):
        count = 1
        while count<=sec:
                GPIO.output(BuzzPin,True)
		GPIO.output(GreenPin,True)
		GPIO.output(RedPin,False)
                time.sleep(0.1)
                GPIO.output(BuzzPin,False)
		GPIO.output(GreenPin,False)
		GPIO.output(RedPin,True)
                time.sleep(0.1)
                count = count+1
        GPIO.output(BuzzPin,False)
	GPIO.output(GreenPin,False)
	GPIO.output(RedPin,False)
		
def blinkg(sec):
        count = 1
        while count<=sec:
                GPIO.output(GreenPin,True)
                time.sleep(0.1)
                GPIO.output(GreenPin,False)
                time.sleep(0.1)
                count = count+1
        GPIO.output(GreenPin,False)
def blinkr(sec):
    count = 1
    while count<=sec:
        GPIO.output(RedPin,True)
        time.sleep(0.1)
        GPIO.output(RedPin,False)
        time.sleep(0.1)
        count = count+1
    GPIO.output(RedPin,False)
def blinkalt(sec):
    count = 1
    while count<=sec:
		blinkg(1)
		blinkr(1)
		count = count+1
def warning(sec):
	count = 1
        while count<=sec:
            GPIO.output(RedPin,True)
   	    GPIO.output(BuzzPin,True)
            time.sleep(0.1)
            GPIO.output(RedPin,False)
	    GPIO.output(BuzzPin,False)
            time.sleep(0.1)
            count = count+1
        GPIO.output(RedPin,False)
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
   	            sql="UPDATE `facultytimetable` SET `facultyID`=%s WHERE scheduleid=%s"
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
    i = 0
    print 'Total number of enrolled fingerprints = '+str(count)
    found=0
    while (found<count):
    	if fps.checkEnrolled(i):
 		print 'Fingerprint Count '+str(found)+' is at ID '+str(i)
		found = found+1
	i=i+1
def get_map_prn(id):
        map = json.load(open("./docs/map.json"))
        prn = map[str(id)]
        return prn
def set_map_prn(id,prn):
        map = json.load(open("./docs/map.json"))
        map[str(id)]=prn
        with open("./docs/map.json", 'w') as file:
	        file.write(json.dumps(map, sort_keys=True))
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
def print_time(line):
        t = time.time()
        lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),3)

def set_template(template_name,fps_id):
    text = open("./templates/"+str(template_name)+".txt","rb") 
    template_data = text.readlines() 
    text.close()
    response = fps.setTemplate(id,str(template_data))
    print response
    print 'Templates written to fps successfully'

def power_save():
	LedPin1 = 11
	LedPin2 = 12
        fade = 20
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(LedPin1, GPIO.OUT)
	GPIO.setup(LedPin2, GPIO.OUT)
	fps.setLED(True)
	count = 0
        p1 = GPIO.PWM(LedPin1, 1000)
        p2 = GPIO.PWM(LedPin2, 1000)
        p1.start(0)
        p2.start(0)
	while not fps.isPressFinger():
	        while not fps.isPressFinger() and count<=3:
	                GPIO.output(LedPin2,True)
	                GPIO.output(LedPin1,False)
	                time.sleep(0.2)
	                GPIO.output(LedPin1,True)
	                GPIO.output(LedPin2,False)
	                time.sleep(0.2)
	                count = count+1
	        GPIO.output(LedPin1,False)
	        GPIO.output(LedPin2,False)
	        count = 0
	        while not fps.isPressFinger() and count<=2:
	                b0 = 0
	                b1 = 100
	                while b0 <=100 and b1 >= 0 and not fps.isPressFinger():
	                        p1.ChangeDutyCycle(b0)
	                        p2.ChangeDutyCycle(b1)
	                        b1 -= fade
	                        b0 += fade
	                        time.sleep(0.1)
	                b0=100
	                b1=0
	                while b0 >= 0 and b1 <=100 and not fps.isPressFinger():
	                        p1.ChangeDutyCycle(b0)
	                        p2.ChangeDutyCycle(b1)
	                        b1 += fade;
	                        b0 -= fade;
	                        time.sleep(0.1)
	                count = count+1
