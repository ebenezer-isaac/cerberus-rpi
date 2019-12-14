import pymysql, subprocess, time, json, os, datetime, calendar, RPi.GPIO as GPIO, datetime
from datetime import date
from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
fps = FingerPi()
lcd = LCD()
rtc = RTC()
host = "192.168.0.7"
user = "phpmyadmin"
password = ""
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
    fps.setLED(True)

def delete_fingerprint(id):
    fps.deleteId(id);

def delete_all():
    fps.deleteAll()
    
def backup_templates():
    i = -1
    while (i<=199):
        i=i+1
        if fps.checkEnrolled(i):
            print('Fingerprint found at ID '+str(i))
            print(get_template("backup-id-"+str(i),i))

def identify():
    fps.waitForFinger()
    id = fps.identify()
    print(id)
    if int(id)==200:
        clrscr()
        beep(2)
        return 0
    else:
        print(id)
        return get_map_prn(id)

def enroll(user_id,template_id):
    lcd.clrscr()
    lcd.println("Enroll Start")
    lcd.println(""+str(user_id))
    lcd.println(""+str(template_id))
    sleep(1000)
    trialCount=0
    id=0
    flag=0
    while id<=149:
        if not fps.checkEnrolled(id):
            break
        else:
            id = id+1
    while trialCount<=2:
        print enroll_main(id)
        verifyCount=0
        while verifyCount<=2:
            lcd.clrscr()
            lcd.println("Press Finger")
            lcd.println("to Verify")
            if fps.identify()==id:
                lcd.clrscr()
                lcd.println("Verification")
                lcd.println("Successfull")
                trialCount=3
                verifyCount=4
                flag=1
                get_template(str(user_id)+"-"+str(template_id),id)
                text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','rb')
                template = text.read()
                text.close()
                upload_template(user_id,template_id)
            else:
                lcd.clrscr()
                lcd.println("Verification")
                lcd.println("UnSuccessfull")
                lcd.println("Try Again")
                verifyCount=verifyCount+1
        if verifyCount==3:
            fps.deleteId(id)
            trialCount=trialCount+1
    if flag==0:
        lcd.println("Enroll Failed")
    fps.deleteId(id)

def enroll_main(id):
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
            sleep(1000)
    fps.setLED(False)
    return response

def print_enrolled():
    count = fps.countEnrolled()
    i = 0
    print("Total number of enrolled fingerprints = "+str(count))
    found=0
    while (found<count):
        if fps.checkEnrolled(i):
             print("Fingerprint Count "+str(found)+" is at ID "+str(i))
             found = found+1
        i=i+1

def get_timeId(time=datetime.datetime.now().strftime("%H:%M:%S")):
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
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
                myconn.commit()
                return get_timeId(time)
            except pymysql.Error as err:
                print(format(err))
                return 0
        myconn.close()
    except pymysql.Error as err:
        print(format(err))
        return 0
    return timeid

def get_dateId(date=date.today
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
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
                myconn.commit()
                return get_dateId(date)
            except pymysql.Error as err:
                print(format(err))
                return 0
        myconn.close()
    except pymysql.Error as err:
        print(format(err))
    return dateid

def get_weekId(week=datetime.datetime.now().isocalendar()[1],year=datetime.datetime.now().year):
    myconn = pymysql.connect(host,user,password,database)
	cur = myconn.cursor() 
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
                myconn.commit()
                return get_weekId(week,year)
            except pymysql.Error as err:
                print(format(err))
                return 0
        myconn.close()
    except pymysql.Error as err:
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
        return 0
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
                return slots[slotid]
        return 1

def sync_all():
    sync_timetable(1,1)
    sync_slots()
    sync_stud_sub()
    sync_stud_det()

def sync_attendance():
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
    flag=0
    with open('./docs/attendance.txt', "r") as fp:
        for i in fp.readlines():
            attendance = i.strip()
            attendance = attendance.split(",")
            timeid=get_timeId(attendance[1])
            scheduleid=attendance[0]
            if len(attendance[2])==16:
                sql="insert into `attendance` values(null,'"+str(attendance[2])+"',"+str(scheduleid)+","+str(timeid)+")"    
            else:
                sql="insert into `facultytimetable` values("+str(scheduleid)+","+str(attendance[2])+")"
            try:
                print(sql)
                cur.execute(sql)
                myconn.commit()
                flag=1
            except:
                flag=0
    if flag==1:
        file = open('./docs/attendance.txt', "w")
        file.write(" ")
        file.close()

def sync_timetable(week=0,year=0):
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
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
                except pymysql.Error as err:
                    print(format(err))
        except pymysql.Error as err:
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
        except pymysql.Error as err:
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
        except pymysql.Error as err:
            print(format(err))

def sync_slots():
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
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
    except pymysql.Error as err:
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
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
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
    except pymysql.Error as err:
        print(format(err))

def att_valid(prn,subjectid,batchid):
    with open('./docs/stud-sub.txt', "r") as fp:
        for x in fp.readlines():
            x = x.split(",")
            x[2] = x[2].replace("\n","")
            if x[0]==str(prn) and x[1]==str(subjectid) and x[2]==str(batchid):
                return True
    return False

def sync_stud_det():
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
    try:
        sql = "select  rollcall.classID, rollcall.rollNo, student.prn from student inner join rollcall on student.PRN = rollcall.PRN"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            file = open("./docs/stud-det.txt","w")
            file.write("")
            file.close()
            file = open("./docs/stud-det.txt","a")
			meta_template = json.load(open("./docs/meta_template.json"))
			for x in result:
                file.write(str(x[0])+","+str(x[1])+","+str(x[2])+"\n")
				template_name=str(x[2])+"-1"
				if template_name not in meta_template:
					meta_template[str(template_name)]="1970-01-01,00:00:00,0"
				template_name=str(x[2])+"-1"
				if template_name not in meta_template:
					meta_template[str(template_name)]="1970-01-01,00:00:00,0"
            file.close()
			with open("./docs/meta_template.json", 'w') as file:
				file.write(json.dumps(meta_template, sort_keys=True))
    except pymysql.Error as err:
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
    print('deleting templates')
    while id<=149:
        print(id)
        fps.deleteId(id)
        id = id+1
    id=0
    print('printing students')
    print(studs)
    for x in studs:
        template_id=1
        print(x)
        while template_id<3:
            try:
                template = open(str(x)+"-"+str(template_id)+".txt")
                template.close()
                set_template(str(x)+"-"+str(template_id),id)
                set_map_prn(id,x)
            except IOError:
                print("file does not exist")
                #pass
            template_id=template_id+1
        id=id+1
	
def upload_template(user_id,template_id, dateid, timeid):
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
    text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','rb')
    template = text.read()
    text.close()
    if len(user_id)==16:   
        sql="""update `studentfingerprint` set `template`= %s, `dateID` = %s, `timeID`=%s where `prn`=%s and `templateID`=%s"""
    else:
        sql="""update `facultyfingerprint` set `template`= %s, `dateID` = %s, `timeID`=%s where `prn`=%s and `templateID`=%s"""
    try:
        val = (dateid,timeid,template,user_id,template_id)
        cur.execute(sql,val)
        myconn.commit()
		myconn.close()
        print "Uploaded Successfully"
    except pymysql.Error as err:
        print err

def download_template(user_id, template_id):
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
    if len(user_id)==16:
        sql="select template, dateID, timeID from studentfingerprint where prn='"+str(user_id)+"' and templateID="+str(template_id)
    else:
        sql="select template, dateID, timeID from facultyfingerprint where facultyID="+str(user_id)+" and templateID="+str(template_id)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for y in result:
            template=y[0]
            print template
            text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','wb')
            text.write(str(template))
            text.close()
			set_meta_temp_dateTimeStatus(user_id,template_id,y[1],y[2],1)
		myconn.close()
    except pymysql.Error as err:
        print err

def delete_template(user_id, template_id):
	os.remove('./templates/'+str(user_id)+"-"+str(template_id)+'.txt')
	meta_template = json.load(open("./docs/meta_template.json"))
    meta_template.pop(str(user_id)+"-"+str(template_id), None)
    with open("./docs/meta_template.json", 'w') as file:
        file.write(json.dumps(meta_template, sort_keys=True))
		
def sync_templates ():
    myconn = pymysql.connect(host,user,password,database)
    cur = myconn.cursor() 
    try:
        sql="select concat(studentfingerprint.PRN,'-',studentfingerprint.templateID) as template_name, (select datedata.date from datedata where studentfingerprint.dateID = datedata.dateID) as Date , (select timedata.time from timedata where studentfingerprint.timeID = timedata.timeID) as Time, case when studentfingerprint.template is null then '0' when studentfingerprint.template is not null then '1' end as status from studentfingerprint union all select concat(facultyfingerprint.facultyID,'-',facultyfingerprint.templateID) as template_name, (select datedata.date from datedata where facultyfingerprint.dateID = datedata.dateID) as Date , (select timedata.time from timedata where facultyfingerprint.timeID = timedata.timeID) as Time, case when facultyfingerprint.template is null then '0' when facultyfingerprint.template is not null then '1' end as status from facultyfingerprint ORDER BY template_name;"
        cur.execute(sql)
        result = cur.fetchall()
		templates=[]
        for x in result:
			templates.append(x[0])
            template_name=x[0]
            db_date = x[1]
            db_time = x[2]
			db_status = x[3]
			dateTimeStatus = get_meta_temp_dateTimeStatus(template_name)
			dateTimeStatus = dateTimeStatus.split(",")
			rpi_date = dateTimeStatus[0]
			rpi_time = dateTimeStatus[1]
			rpi_status = dateTimeStatus[2]
			if db_date==rpi_date and db_time==rpi_time:
				pass
			else:
				template_name = template_name.split("-")
				user_id=template_name[0]
				template_id=template_name[1]
				time_sort=[rpi_date+" "+rpi_time,db_date+" "+db_time]
				time_sort.sort()
				if db_status==0 and rpi_status==0:
					pass
				elif db_status==0 and rpi_status==1:
					if time_sort[0]==db_status:
						delete_template(user_id,template_id,db_date,db_time)
					else:
						upload_template(user_id, template_id,rpi_date,rpi_time)
				elif db_status==1 and rpi_status==0:
						download_template(user_id,template_id)
				elif db_status==1 and rpi_status==1:
					if time_sort[0]==db_status:
						download_template(user_id,template_id)
					else:
						upload_template(user_id, template_id,rpi_date,rpi_time)
		#delete all templates except for templates in list				
    except pymysql.Error as err:
        print(format(err))

#---------------Utilities---------------------------------------

def get_map_prn(id):
    map = json.load(open("./docs/map.json"))
    prn = map[str(id)]
    return prn

def set_map_prn(id,prn):
    map = json.load(open("./docs/map.json"))
    map[str(id)]=prn
    with open("./docs/map.json", 'w') as file:
        file.write(json.dumps(map, sort_keys=True))
		
def get_meta_temp_dateTimeStatus(template_name):
    meta_template = json.load(open("./docs/meta_template.json"))
    dateTimeStatus = meta_template[str(template_name)]
    return dateTimeStatus

def set_meta_temp_dateTimeStatus(user_id,template_id,date,time,status):
	dateTimeStatus=str(date)+","+str(time)+","+str(status)
    meta_template = json.load(open("./docs/meta_template.json"))
    meta_template[str(template_name)]=dateTimeStatus
    with open("./docs/meta_template.json", 'w') as file:
        file.write(json.dumps(meta_template, sort_keys=True))

def get_template(template_name,fps_id):
    response=fps.getTemplate(fps_id)
    template=open("./templates/"+str(template_name)+".txt","wb")
    template.write(str(response))
    template.close()
    print("Template written to "+str(template_name)+".txt")

def set_template(template_name,fps_id):
    text = open("./templates/"+str(template_name)+".txt","rb")
    template_data = text.read()
    text.close()
    print(template_data)
    response = fps.setTemplate(fps_id,str(template_data))
    print('Templates written to fps successfully')

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
