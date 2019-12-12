import mysql.connector, subprocess, time, json, os, datetime, calendar, RPi.GPIO as GPIO, datetime
from datetime import date
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
print("trying for connection")
#myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)
#cur = myconn.cursor()
print("got connection")
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

def get_timeId(time=datetime.datetime.now().strftime("%H:%M:%S")):
    timeid = 0
    try:
        sql="SELECT timeID from timedata where time = '"+str(time)+"'"
        cur.execute(sql)
        result = cur.fetchall()
        for x in result:
            timeid=x[0]
        if timeid==0:
            try:
                sql="insert into timedata values(null,'"+str(time)+"')"
                val = (time)
                cur.execute(sql,val)
                return get_timeId(time)
            except mysql.connector.Error as err:
                print(format(err))
                return 0
    except mysql.connector.Error as err:
        print(format(err))
        return 0
    return timeid

def get_dateId(date=date.today()):
    dateid = 0
    try:
        sql="SELECT dateID from datedata where date = '"+str(date)+"'"
        cur.execute(sql)
        result = cur.fetchall()
        for x in result:
            dateid=x[0]
        if dateid==0:
            try:
                sql="insert into datedata values(null,'"+str(date)+"')"
                cur.execute(sql)
                return get_dateId(date)
            except mysql.connector.Error as err:
                print(format(err))
                return 0
    except mysql.connector.Error as err:
        print(format(err))
    return dateid

def get_weekId(week=datetime.datetime.now().isocalendar()[1],year=datetime.datetime.now().year):
    weekid = 0
    try:
        sql="SELECT weekID from week where week = "+str(week)+" and year = "+str(year)
        cur.execute(sql)
        result = cur.fetchall()
        for x in result:
            weekid=x[0]
        if weekid==0:
            try:
                sql="insert into week values(null,"+str(week)+","+str(year)+")"
                cur.execute(sql)
                return get_weekId(week,year)
            except mysql.connector.Error as err:
                print(format(err))
                return 0
    except mysql.connector.Error as err:
        print(format(err))
        return 0
    return weekid

def get_slotId(time=datetime.datetime.now().strftime("%H:%M:%S")):
    with open('./docs/slots.txt', "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[2] = x[2].replace("\n","")
            if x[1]<time<x[2]:
                return x[0]
    return 0

def get_scheduleId(slotid=get_slotId(),week=datetime.datetime.now().isocalendar()[1],year=datetime.datetime.now().year,dayid=datetime.datetime.now().weekday()+1):
    with open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt", "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[5] = x[5].replace("\n","")
            if x[1]==str(slotid) and x[2]==str(dayid):
                return x[0]
    return 0

def get_next_scheduleId():
    week=datetime.datetime.now().isocalendar()[1]
    year=datetime.datetime.now().year
    dayid=datetime.datetime.now().weekday()+1
    today=[]
    with open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt", "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[5] = x[5].replace("\n","")
            print(x)
            if x[2]==str(dayid):
                temp = []
                temp.append(x[1])
                temp.append(x[3])
                temp.append(x[4])
                temp.append(x[5])
                today.append(temp)
    if len(today)==0:
        return 'No Labs Today'
    else:
        today.sort()
        time=datetime.datetime.now().strftime("%H:%M:%S")
        slots=[]
        with open('./docs/slots.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                slots.append(x)
        slots.sort()
        for x in today:
            slotid=int(x[0])
            if slots[slotid][1]>time:
                return 'Next Lab at '+str(slots[slotid][1])  
        return 'All Labs Over'

def sync_attendance():
    with open('./docs/attendance.txt', "r") as fp:
        for i in fp.readlines():
            attendance = i.strip()
            attendance = attendance.split(",")
            timeid=get_timeId(attendance[1])
            scheduleid=attendance[0]
            if len(attendance[2])==16:
                try:
                    sql="insert into `attendance` values(null,'"+str(attendance[2])+"',"+str(scheduleid)+","+str(timeid)+")"
                    print(sql)
                    cur.execute(sql)
                except mysql.connector.Error as err:
                    print(format(err))
            else:
                try:
                    sql="insert into `facultytimetable` values("+str(scheduleid)+","+str(attendance[2])+")"
                    print(sql)
                    cur.execute(sql)
                except mysql.connector.Error as err:
                    print(format(err))

def sync_timetable(week=0,year=0):
    if week==0 and year==0:
        try:
            sql = "select weekid,week,year from week order by weekid"
            cur.execute(sql)
            result = cur.fetchall()
            for x in result:
                try:
                    sql = "select timetable.scheduleID, slot.slotId, timetable.dayID, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(x[0])+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
                    cur.execute(sql)
                    result = cur.fetchall()
                    file = open("./timetables/timetable-"+str(x[1])+"-"+str(x[2])+".txt","w")
                    file.write("")
                    file.close()
                    if result:
                        file = open("./timetables/timetable-"+str(x[1])+"-"+str(x[2])+".txt","a")
                        for y in result:
                            file.write(str(y[0])+","+str(y[1])+","+str(y[2])+","+str(y[3])+","+str(y[4])+","+str(y[5])+"\n")
                        file.close()
                except mysql.connector.Error as err:
                    print(format(err))
        except mysql.connector.Error as err:
            print(format(err))
    elif week==1 and year==1:
        week= datetime.datetime.now().isocalendar()[1]
        year = datetime.datetime.now().year
        try:
            sql = "select timetable.dayID, slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(get_weekId(week,year))+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
            cur.execute(sql)
            result = cur.fetchall()
            file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","w")
            file.write("")
            file.close()
            if result:
                file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","a")
                for y in result:
                    file.write(str(y[0])+","+str(y[1])+","+str(y[2])+","+str(y[3])+","+str(y[4])+","+str(y[5])+"\n")
                file.close()
        except mysql.connector.Error as err:
            print(format(err))
    else:
        try:
            sql = "select timetable.dayID, slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(get_weekId(week,year))+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
            cur.execute(sql)
            result = cur.fetchall()
            file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","w")
            file.write("")
            file.close()
            if result:    
                file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","a")
                for y in result:
                    file.write(str(y[0])+","+str(y[1])+","+str(y[2])+","+str(y[3])+","+str(y[4])+","+str(y[5])+"\n")
                file.close()
        except mysql.connector.Error as err:
            print(format(err))

def sync_slots():
    try:
        sql = "select * from slot order by startTime"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            file = open("./docs/slots.txt","w")
            file.write("")
            file.close()
            file = open("./docs/slots.txt","a")
            for x in result:
                file.write(str(x[0])+","+str(x[1])+","+str(x[2])+"\n")
            file.close()
    except mysql.connector.Error as err:
        print(format(err))

def get_map_prn(id):
        map = json.load(open("./docs/map.json"))
        prn = map[str(id)]
        return prn

def set_map_prn(id,prn):
        map = json.load(open("./docs/map.json"))
        map[str(id)]=prn
        with open("./docs/map.json", 'w') as file:
            file.write(json.dumps(map, sort_keys=True))

def sync_stud_sub():
    try:
        sql = "select * from studentsubject order by prn"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            file = open("./docs/stud-sub.txt","w")
            file.write("")
            file.close()
            file = open("./docs/stud-sub.txt","a")
            for x in result:
                file.write(str(x[0])+","+str(x[1])+","+str(x[2])+"\n")
            file.close()
    except mysql.connector.Error as err:
        print(format(err))

def att_valid(prn,subjectid,batchid):
    with open('./docs/stud-sub.txt', "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[2] = x[2].replace("\n","")
            if x[0]==str(prn) and x[1]==str(subjectid) and x[2]==str(batchid):
                return True
    return False
att_valid(2017033800104112,'BCA1538',2)

def sync_stud_det():
    try:
        sql = "select  rollcall.classID, rollcall.rollNo, student.prn from student inner join rollcall on student.PRN = rollcall.PRN"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            file = open("./docs/stud-det.txt","w")
            file.write("")
            file.close()
            file = open("./docs/stud-det.txt","a")
            for x in result:
                file.write(str(x[0])+","+str(x[1])+","+str(x[2])+"\n")
            file.close()
    except mysql.connector.Error as err:
        print(format(err))

def get_stud_sub_list(subjectid, batchid):
    studs=[]
    with open('./docs/stud-sub.txt', "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[2] = x[2].replace("\n","")
            if x[1]==str(subjectid) and x[2]==str(batchid):
                studs.append(x[0])
    return studs

def set_templates(studs):
    id=0
    #delete templates till 150
    for x in studs:
        #set_template(id,x)
        #set_map_prn(id,x)
        id=id+1

def sync_templates ():
    myconn = mysql.connector.connect(host=host, user=user,passwd=password,database=database)
    cur = myconn.cursor()
    text = open("./docs/logid.txt","r")
    logid =str(text.read()).strip()
    text.close()
    sync = []
    with open('./docs/sync.txt', "r") as fp:
        for i in fp.readlines():
            tmp = i.strip()
            tmp = tmp.split(",")
            try:
                sync.append((tmp[0], tmp[1], tmp[2], tmp[3]))
            except:
                pass
    try:
        sql="SELECT logID, (select datedata.date from datedata,log where log.dateID=datedata.dateID) as date ,(select timedata.time from timedata,log where log.timeID=timedata.timeID)as time, comments FROM `log` where logTypeID=1 and logID>"+str(logid)
        print(sql)
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
    print(sync)
    for x in sync:
        tmp = str(x[0]).split(" ")
        date = tmp[0]
        time = tmp[1]
        dateid = get_dateId(date)
        timeid = get_timeId(time)
        template_name = x[1]
        temp = str(template_name).split('-')
        user_id = temp[0]
        template_id = temp[1]
        status = x[2]
        source = x[3]
        if source=='rpi':
            if status=='delete':
                if len(user_id)==16:
                    sql="delete * from studentfingerprint where prn='"+str(user_id)+"' and templateID="+str(template_id)
                else:
                    sql="delete * from facultyfingerprint where facultyID="+str(user_id)+" and templateID="+str(template_id)
                try:
                    cur.execute(sql)
                    sql="insert into log values(null,1,"+str(dateid)+",'"+str(timeid)+","+str(template_name)+" delete')"
                    cur.execute(sql)
                except mysql.connector.Error as err:
                    print(format(err))
            elif status=='enroll':
                if len(user_id)==16:
                   sql="insert into studentfingerprint values('"+str(user_id)+"', "+str(template_id)+", "+str(template)+")"
                else:
                   sql="insert into facultyfingerprint values("+str(user_id)+", "+str(template_id)+", "+str(template)+")"
                text = open('./templates/'+str(template_name)+'.txt','rb')
                template = text.read()
                text.close()
                try:
                    cur.execute(sql)
                    sql="insert into log values(null,1,"+str(dateid)+",'"+str(timeid)+","+str(template_name)+" enroll')"
                    cur.execute(sql)
                except mysql.connector.Error as err:
                    print(format(err))
        elif source=='db':
            if status=='delete':
                os.remove('./templates/'+str(template_name)+'.txt')
                map = json.load(open("./docs/map.json"))
                for fps_id in map:
                    if map[id]==str(template_name):
                        fps.DeleteId(id)
                        mps[id]='0'
            elif status=='enroll':
                if len(user_id)==16:
                    sql="select template from studentfingerprint values where prn='"+str(user_id)+"' and templateID="+str(template_id)
                else:
                    sql="select template from facultyfingerprint values where facultyID="+str(user_id)+" and templateID="+str(template_id)
                try:
                    cur.execute(sql)
                    fingerprints = cur.fetchall()
                    for y in result:
                        template=y[0]
                        text = open('/templates/'+str(template_name)+'.txt','wb')
                        text.write(str(template))
                        text.close()
                except:
                    myconn.rollback()
    text = open("./docs/logid.txt","w")
    text.write(str(logid))
    text.close()

#---------------Utilities---------------------------------------

def get_map_prn(id):
        map = json.load(open("./docs/docs/map.json"))
        prn = map[str(id)]
        return prn

def set_map_prn(id,prn):
        map = json.load(open("./docs/docs/map.json"))
        map[str(id)]=prn
        with open("./docs/docs/map.json", 'w') as file:
	        file.write(json.dumps(map, sort_keys=True))

def set_template(template_name,fps_id):
    text = open("./templates/"+str(template_name)+".txt","rb")
    template_data = text.readlines()
    text.close()
    response = fps.setTemplate(id,str(template_data))
    print response
    print 'Templates written to fps successfully'

def println(text):
	lcd.println(text)

def printline(text,line):
	lcd.println(text,line)

def clrscr():
	lcd.clrscr()

def sleep(milsec):
    time.sleep(milsec/1000)

def print_time(line):
        t = time.time()
        lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),3)

def getKeyPress():
    for  j in range(4):
        GPIO.output(COL[j],0)
        for i in range(4):
            if GPIO.input(ROW[i])==0:
                while (GPIO.input(ROW[i])==0):
                    time.sleep(0.2)
                return MATRIX[i][j]
        GPIO.output(COL[j],1)

def getKey():
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

#-------------------------Lighting------------------------------------

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
