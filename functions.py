import pymysql, subprocess, time, json, os, datetime, calendar, RPi.GPIO as GPIO, datetime, socket
from datetime import date
from drivers.fingerpi import FingerPi
from drivers.lcd import LCD
from drivers.rtc import RTC
fps = FingerPi()
lcd = LCD()
rtc = RTC()
host = "172.21.170.14"
user = "cerberus"
password = "abc@123"
database = "cerberus"
labid = 1
BuzzPin =36
GreenPin = 26
RedPin = 18
MATRIX = [ [1,2,3,'A'], [4,5,6,'B'], [7,8,9,'C'], ['*',0,'#','D'] ]
COL = [32,37,33,31]
ROW = [29,15,13,11]

def setup():
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(BuzzPin, GPIO.OUT)
        GPIO.setup(GreenPin, GPIO.OUT)
        GPIO.setup(RedPin, GPIO.OUT)
        while not fps.open:
            fps.open()
        fps.setLED(True)
        sleep(250)
        fps.setLED(False)
        for j in range(4):
            GPIO.setup(COL[j], GPIO.OUT)
            GPIO.output(COL[j],1)
        for i in range(4):
            GPIO.setup(ROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)
        beep(4);
        return True
    except Exception as e:
        print(e)
        return False

def main_menu():
    clrscr()
    println("Main Menu")
    println("Setting up")
    println("Fingerprints")
    sleep(1000)
    auth_result  = authorization()
    print 'back in main'
    print auth_result
    while not auth_result:
        clrscr()
        println("Canceled")
        sleep(1000)
        return
    clrscr()
    println(str(auth_result[2]))
    println("Authorized")
    println("<<>>")
    blinkg(3)
    sleep(1000)
    clrscr()
    while True:
        clrscr()
        printleft("A- Check Connection")
        printleft("B- Sync Now")
        printleft("C- Enroll")
        printleft("#- Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            println("Check Connection")
            printIP()
            if check_conn():
                println("Connection")
                println("Available")
                sleep(1500)
            else:
                clrscr()
                println("Connection")
                println("Unavailable")
                printIP()
                println("Press Any Key")
                key = getKey()
        elif key == 'B':
            sync_all()
        elif key == 'C':
            println("Enroll Fingerprint")
            sleep(1000)
            enroll_menu()
            return
        elif key == '#':
            print 'exit main menufunction'
            return
        else:
            println("Invalid Input")
            sleep(1500)

def enroll_menu():
    delete_all()
    while True:
        clrscr()
        printleft("A - ContRegistration")
        printleft("B - SeleRegistration")
        printleft("C - Add Admin")
        printleft("# - Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            enroll_cont()
            return
        elif key == 'B':
            enroll_sele()
            return
        elif key == 'C':
            faculty_enroll()
            return
        elif key == '#':
            return
        else:
            println("Invalid Input")
            sleep(1500)

def enroll_cont():
    clrscr()
    println("Autonomous")
    println("Enrollment")
    while not fps.open:
        fps.open()
    fps.setLED(True)
    println("A to Continue")
    println("Any Key to Abort")
    key = getKey()
    clrscr()
    if key == 'A':
        classID = get_class()
        studs = get_class_studs(classID)
        index = 0
        while -1< index < len(studs):
            clrscr()
            println("Roll Number :" + str(studs[index][1]))
            println("A- Continue")
            println("B- Skip    C- Prev")
            println("Any to Abort")
            key = getKey()
            if key == 'A':
                id = 1
                while id<3:
                    clrscr()
                    if check_template(prn,id):
                        println("Fingerprint "+str(id))
                        println("Already")
                        println("Exists")
                        sleep(1000)
                    else:
                        clrscr()
                        println("PRN:"+str(prn))
                        println("Fingerprint "+str(id))
                        println("Press A to Continue")
                        println("Any Key to Skip")
                        key = getKey()
                        if key == 'A':
	                    enroll(studs[index][0],id)
                    id = id +1
            elif key == 'B':
                pass
            elif key == 'C':
                if not index==0:
                    index = index -2
            else:
                clrscr()
                println("Exiting")
                sleep(500)
                fps.setLED(False)
                return
            index = index+1
        clrscr()
        println("All Students Over")  
        sleep(1000)
    else:
        clrscr()
        println("Exiting")
        sleep(500)
        fps.setLED(False)
        return

def enroll_sele():
    clrscr()
    println("Selected PRN")
    println("Enrollment")
    while not fps.open:
        fps.open()
    fps.setLED(True)
    while True:
        clrscr()
        println("Selected PRN")
        println("Enrollment")
        println("Press A to Continue")
        println("Any Key to Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            prn = get_prn()
            id = 1
            while id<3:
                clrscr()
                if check_template(prn,id):
                    println("Fingerprint "+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    clrscr()
                    println("PRN:"+str(prn))
                    println("Fingerprint "+str(id))
                    println("Press A to Continue")
                    println("Any Key to Skip")
                    key = getKey()
                    if key == 'A':
                        enroll(prn,id)
                id = id +1
        else:
            clrscr()
            println("Exiting")
            sleep(500)
            fps.setLED(False)
            return

def faculty_enroll():
    clrscr()
    println("Faculty")
    println("Enrollment")
    while not fps.open:
        fps.open()
    fps.setLED(True)
    while True:
        clrscr()
        println("Faculty")
        println("Enrollment")
        println("Press A to Continue")
        println("Any Key to Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            faculty_id = get_faculty_id()
            id = 1
            while id<3:
                clrscr()
                if check_template(faculty_id,id):
                    println("Fingerprint"+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    enroll(faculty_id,id)
                id = id +1
        else:
            clrscr()
            println("Exiting")
            sleep(500)
            fps.setLED(False)
            return

def check_template(user_id,template_id):
    try:
        text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','r')
        template = text.read()
        text.close()
        return True
    except Exception as e:
        print e
        return False

def authorization(schedule_id = 0, type =0):
    clrscr()
    println("Setting Up")
    println("Student")
    println("Fingerprints")
    delete_all()
    set_fac_templates()
    clrscr()
    println("Authorization")
    if type==1:
        println("Required for Lab")
        println("Press Finger")
        println("# for Menu")
    else:
        println("Required for Menu")
        println("Press Finger")
        println("# to Cancel")
    print 'inside authorization'
    while not fps.open:
        print 'fps open'
        fps.open()
        print 'fps light'
    fps.setLED(True)
    faculty_id = 0
    while True:
        id = 0
        key = getKeyPress()
        if fps.isPressFinger():
            if fps.captureFinger(False):
                if fps.sendCommand('Identify'):
                    response = [fps.getResponse(), None]
                    if len(str(response[0]['Parameter']))>3:
                        response[0]['Parameter']='200'
                    id = response[0]['Parameter']
                    if 200>id>149:
                        print id
                        faculty_id = get_map_prn(id)
                        print "fac" +str(faculty_id)
                        faculty_name = get_fac_name(faculty_id)
			print faculty_name
                        clrscr()
                        println("Finger")
                        println("Found")
                        println("Connecting DB")
                        if not schedule_id == 0:
                            start_lab(schedule_id,faculty_id)
                        print [True,faculty_id, faculty_name]
                        fps.setLED(False)
                        return [True,faculty_id, faculty_name]
                    else:
                        clrscr()
                        println("Faculty")
                        println("Required")
                        println("to")
                        println("Authorize")
                        blinkr(3)
                        sleep(1000)
                        clrscr()
                        println("Authorization")
		        if type==1:
    		            println("Required for Lab")
		            println("Press Finger")
		            println("# for Menu")
		        else:
		            println("Required for Menu")
                            println("Press Finger")
                            println("# to Cancel")
            else:
                clrscr()
		println("Finger Capture")
		println("Failed")
		println("Try Again")
                blinkr(3)
                sleep(1000)
                clrscr()
                println("Authorization")
	        if type==1:
	            println("Required for Lab")
                    println("Press Finger")
                    println("# for Menu")
	        else:
                    println("Required for Menu")
                    println("Press Finger")
                    println("# to Cancel")
        else:
            if key=='#':
                fps.setLED(False)
                return False
            else:
                pass

def take_attendance(schedule_id,endtime, abbr, batch,studs):
    clrscr()
    println("Setting")
    println("Up")
    println("Fingerprints")
    delete_all()
    set_stud_templates(studs)
    clrscr()
    println("Subject :")
    println(str(abbr))
    println("Batch :"+str(batch))
    while not fps.open:
        fps.open()
    fps.setLED(True)
    println("Press Finger")
    while datetime.datetime.now().strftime("%H:%M:%S")<endtime: 
        id = 0
        key = getKeyPress()
        if fps.isPressFinger():
            if fps.captureFinger(False):
                if fps.sendCommand('Identify'):
                    response = [fps.getResponse(), None]
                    if len(str(response[0]['Parameter']))>3:
                        response[0]['Parameter']='200'
                    id = response[0]['Parameter']
                    if 0<id<150:
                        clrscr()
                        println("Finger")
                        println("Identified")
                        blinkg(3)
                        sleep(1000)
                        prn = get_map_prn(id)
                        clrscr()
                        println("PRN:"+str(prn))
                        println("")
                        println("Inserting Att")
                        sleep(1000)
                        insert_attendance(schedule_id,prn)
                    else:
                        clrscr()
                        println("Finger")
                        println("Not Found")
                        println("Try Again")
                        blinkr(3)
                        sleep(1000)
                        clrscr()
                        println("Subject :")
                        println(str(abbr))
                        println("Batch :"+str(batch))
                        println("Press Finger")
            else:
                clrscr()
		println("Finger Capture")
		println("Failed")
		println("Try Again")
                sleep(1000)
                clrscr()
                println("Subject :")
                println(str(abbr))
                println("Batch :"+str(batch))
                println("Press Finger")
        else:
            if key=='#':
                main_menu()
                clrscr()
                println("Subject :")
                println(str(abbr))
                println("Batch :"+str(batch))
                println("Press Finger")
                while not fps.open:
                    fps.open()
                fps.setLED(True)
            else:
                pass
    fps.setLED(False)

def get_class_studs(classID):
    studs=[]
    try:
        with open('./docs/stud-det.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                if x[0]==str(classID):
                    studs.append([x[2],x[1]])
        return studs
    except Exception as e:
        print(e)
        return False

def delete_fingerprint(id):
    try:
        fps.deleteId(id);
        return True
    except Exception as e:
        print(e)
        return False

def delete_all():
    try:
        fps.deleteAll()
        return True
    except Exception as e:
        print(e)
        return False
    
def backup_templates():
    try:
        i = -1
        while (i<=199):
            i=i+1
            if fps.checkEnrolled(i):
                print('Fingerprint found at ID '+str(i))
                print(get_template("backup-id-"+str(i),i))
        return True
    except Exception as e:
        print(e)
        return False
    
def identify():
    try:
        fps.waitForFinger()
        id = fps.identify()
        print(""+str(id))
        if int(id)==200:
            clrscr()
            beep(2)
            return 0
        else:
            print(id)
            return get_map_prn(id)
    except Exception as e:
        print('error here')
        print(e)
        return False

def print_enrolled():
    try:
        count = fps.countEnrolled()
        i = 0
        print("Total number of enrolled fingerprints = "+str(count))
        found=0
        while (found<count):
            if fps.checkEnrolled(i):
                print("Fingerprint Count "+str(found)+" is at ID "+str(i))
                found = found+1
            i=i+1
        return True
    except Exception as e:
        print(e)
        return False

def get_slotId(time=datetime.datetime.now().strftime("%H:%M:%S")):
    try:
        with open('./docs/slots.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                if x[1]<time<x[2]:
                    return x[0]
        return 0
    except Exception as e:
        print(e)
        return 0

def get_next_schedule():
    try:
        week=datetime.datetime.now().isocalendar()[1]
        year=datetime.datetime.now().year
        dayid=datetime.datetime.now().weekday()+1
#        week = 1
#        year = 2020
#        dayid = 3
        today=[]
        try:
            with open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt", "r") as fp:
                for x in fp.readlines():
                    x = x.split(",")
                    x[len(x)-1] = x[len(x)-1].replace("\n","")
                    if x[1]==str(dayid):
                        x.pop(1)
                        today.append(x)
        except Exception as e:
            print(e)
            return -1
        if len(today)==0:
            return 3
        else:
            today.sort()
            time=datetime.datetime.now().strftime("%H:%M:%S")
#            time = '13:01:00'
            for x in today:
                if x[1]<=time<=x[2]:
                    return [0,x]
            for x in today:
                if x[2]>time:
                    return [1,x]
            return 2
    except Exception as e:
        print(e)
        return False

def att_valid(prn,subjectid,batchid):
    try:
        with open('./docs/stud-sub.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                if x[0]==str(prn) and x[1]==str(subjectid) and x[2]==str(batchid):
                    return True
        return False
    except Exception as e:
        print(e)
        return False

def get_stud_sub_list(subjectid, batchid):
    studs=[]
    try:
        with open('./docs/stud-sub.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                if x[1]==str(subjectid) and x[2]==str(batchid):
                    studs.append(x[0])
        return studs
    except Exception as e:
        print(e)
        return False

#---------------Sync---------------------------------------	

def sync_all():
    clrscr()
    println("Syncing DB")
    println("<<>>")
    if check_conn():
        sync_timetable(1,1)
        sync_slots()
        sync_class()
        sync_fac_det()
        sync_stud_det()
        sync_stud_sub()
        sync_attendance()
        sync_templates()
        print 'outside sync function'
        clrscr()
        println("Sync Success")
        println("Connection")
        println("Available")
        sleep(1500)
    else:
        clrscr()
        println("Sync Failed")
        println("Connection")
        println("Unavailable")
        sleep(1500)
    week=datetime.datetime.now().isocalendar()[1]
    year=datetime.datetime.now().year
    flag = 0
    clrscr()
    println("Checking")
    println("Timetable")
    try:
        file =  open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt", "r")
        file.close()
        println("Timetable:Found") 
        sleep(1500)
        return True
    except:
        println("Timetable:Error")
        println("Check DB Conn")
        sleep(1500)
        return False

def sync_attendance():
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        flag=1
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
                except Exception as e:
                    error = str(e)
                    if str(e).find('Duplicate entry')==-1:
                        print(e)
                        flag = 0
                    else:
                        pass
        if flag==1:
            print 'erasing'
            file = open('./docs/attendance.txt', "w")
            file.write("")
            file.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def sync_timetable(week=0,year=0):
    try:
        myconn = pymysql.connect(host,user,password,database)
        print("got connection")
        cur = myconn.cursor() 
        if week==0 and year==0:
            try:
                sql = "select weekid,week,year from week order by weekid"
                cur.execute(sql)
                result = cur.fetchall()
                for x in result:
                    try:
                        sql = "select timetable.scheduleID, timetable.dayID, slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(x[0])+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
                        cur.execute(sql)
                        result = cur.fetchall()
                        file = open("./timetables/timetable-"+str(x[1])+"-"+str(x[2])+".txt","w")
                        file.write("")
                        file.close()
                        if result:
                            file = open("./timetables/timetable-"+str(x[1])+"-"+str(x[2])+".txt","a")
                            for y in result:
                                startTime=str(y[2])
                                if len(startTime)==7:
                                    startTime = '0'+startTime
                                endTime=str(y[3])
                                if len(endTime)==7:
                                    endTime = '0'+endTime
                                file.write(str(y[0])+","+str(y[1])+","+startTime+","+endTime+","+str(y[4])+","+str(y[5])+","+str(y[6])+"\n")
                            file.close()
                    except Exception as e:
                        print(e)
                        return False
            except Exception as e:
                print(e)
                return False
        elif week==1 and year==1:
            week= datetime.datetime.now().isocalendar()[1]
            year = datetime.datetime.now().year
            print week
            print year
            try:
                sql = "select timetable.scheduleID, timetable.dayID, slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(get_weekId(week,year))+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
                cur.execute(sql)
                result = cur.fetchall()
                file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","w")
                file.write("")
                file.close()
                if result:
                    file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","a")
                    for y in result:
                        startTime=str(y[2])
                        if len(startTime)==7:
                            startTime = '0'+startTime
                        endTime=str(y[3])
                        if len(endTime)==7:
                            endTime = '0'+endTime
                        file.write(str(y[0])+","+str(y[1])+","+startTime+","+endTime+","+str(y[4])+","+str(y[5])+","+str(y[6])+"\n")
                    file.close()
            except Exception as e:
                print(e)
                return False
        else:
            print 'manual'
            try:
                sql = "select timetable.scheduleID, timetable.dayID, slot.startTime , slot.endTime, timetable.subjectID, timetable.batchID, subject.Abbreviation from timetable inner join slot on timetable.slotID = slot.slotID inner join subject on timetable.subjectID = subject.subjectID where timetable.labID=1 and timetable.weekID="+str(get_weekId(week,year))+"  ORDER BY `timetable`.`dayID` ASC, slot.startTime ASC"
                cur.execute(sql)
                result = cur.fetchall()
                file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","w")
                file.write("")
                file.close()
                if result:
                    file = open("./timetables/timetable-"+str(week)+"-"+str(year)+".txt","a")
                    for y in result:
                        startTime=str(y[2])
                        if len(startTime)==7:
                            startTime = '0'+startTime
                        endTime=str(y[3])
                        if len(endTime)==7:
                            endTime = '0'+endTime
                        file.write(str(y[0])+","+str(y[1])+","+startTime+","+endTime+","+str(y[4])+","+str(y[5])+","+str(y[6])+"\n")
                    file.close()
            except Exception as e:
                print(e)
                return False
        return True
    except Exception as e:
        print(e)
        return False
    
def sync_fac_det():
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        rpi_facs=[]
        rpi_file = open("./docs/fac-det.txt", "r")
        rpi_facs_list = (rpi_file.read().split("\n"))
        rpi_facs_list.pop(len(rpi_facs_list)-1)
        for x in rpi_facs_list:
            x = x.split(",")
            rpi_facs.append(str(x[0]))
        db_facs=[]
        try:
            sql = "select faculty.facultyID, faculty.name from faculty"
            cur.execute(sql)
            result = cur.fetchall()
            if result:
                file = open("./docs/fac-det.txt","w")
                file.write("")
                file.close()
                file = open("./docs/fac-det.txt","a")
                meta_template = json.load(open("./docs/meta_template.json"))
                for x in result:
                    db_facs.append(str(x[0]))
                    file.write(str(x[0])+","+str(x[1])+"\n")
                    template_name=str(x[0])+"-1"
                    if template_name not in meta_template:
                        meta_template[str(template_name)]="1970-01-01,00:00:00,0"
                    template_name=str(x[0])+"-2"
                    if template_name not in meta_template:
                        meta_template[str(template_name)]="1970-01-01,00:00:00,0"
                file.close()
                with open("./docs/meta_template.json", 'w') as file:
                    file.write(json.dumps(meta_template, sort_keys=True))
        except Exception as e:
            print(e)
            return False
        for x in list(set(rpi_facs) - set(db_facs)):
            delete_user(x)
        return True
    except Exception as e:
        print(e)
        return False
    
def sync_stud_det():
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        rpi_studs=[]
        rpi_file = open("./docs/stud-det.txt", "r")
        rpi_studs_list = (rpi_file.read().split("\n"))
        rpi_studs_list.pop(len(rpi_studs_list)-1)
        for x in rpi_studs_list:
            x = x.split(",")
            rpi_studs.append(str(x[2]))
        db_studs=[]
        try:
            sql = "select  rollcall.classID, rollcall.rollNo, student.prn from student inner join rollcall on student.PRN = rollcall.PRN order by LENGTH(rollcall.rollNo),rollcall.rollNo"
            cur.execute(sql)
            result = cur.fetchall()
            if result:
                file = open("./docs/stud-det.txt","w")
                file.write("")
                file.close()
                file = open("./docs/stud-det.txt","a")
                meta_template = json.load(open("./docs/meta_template.json"))
                for x in result:
                    db_studs.append(str(x[2]))
                    file.write(str(x[0])+","+str(x[1])+","+str(x[2])+"\n")
                    template_name=str(x[2])+"-1"
                    if template_name not in meta_template:
                        meta_template[str(template_name)]="1970-01-01,00:00:00,0"
                    template_name=str(x[2])+"-2"
                    if template_name not in meta_template:
                        meta_template[str(template_name)]="1970-01-01,00:00:00,0"
                file.close()
                with open("./docs/meta_template.json", 'w') as file:
                    file.write(json.dumps(meta_template, sort_keys=True))
        except Exception as e:
            print(e)
            return False
        for x in list(set(rpi_studs) - set(db_studs)):
            delete_user(x)
        return True
    except Exception as e:
        print(e)
        return False

def sync_slots():
    try:
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
        except Exception as e:
            print(e)
            return False
        return True
    except Exception as e:
        print(e)
        return False

def sync_class():
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        try:
            sql = "select * from class order by classID"
            cur.execute(sql)
            result = cur.fetchall()
            if result:
                file = open("./docs/class.txt","w")
                file.write("")
                file.close()
                file = open("./docs/class.txt","a")
                for x in result:
                    file.write(str(x[0])+","+str(x[1])+"\n")
                file.close()
        except Exception as e:
            print(e)
            return False
        return True
    except Exception as e:
        print(e)
        return False

def sync_stud_sub():
    try:
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
        except Exception as e:
            print(e)
            return False
        return True
    except Exception as e:
        print(e)
        return False

#---------------Templates---------------------------------------

def sync_templates ():
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        try:
            print('inside sync templates')
            sql="select concat(studentfingerprint.PRN,'-',studentfingerprint.templateID) as template_name, (select datedata.date from datedata where studentfingerprint.dateID = datedata.dateID) as Date , (select timedata.time from timedata where studentfingerprint.timeID = timedata.timeID) as Time, case when studentfingerprint.template is null then '0' when studentfingerprint.template is not null then '1' end as status from studentfingerprint union all select concat(facultyfingerprint.facultyID,'-',facultyfingerprint.templateID) as template_name, (select datedata.date from datedata where facultyfingerprint.dateID = datedata.dateID) as Date , (select timedata.time from timedata where facultyfingerprint.timeID = timedata.timeID) as Time, case when facultyfingerprint.template is null then '0' when facultyfingerprint.template is not null then '1' end as status from facultyfingerprint ORDER BY template_name;"
            cur.execute(sql)
            result = cur.fetchall()
            for x in result:
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
                    rpi_dateTime = str(rpi_date)+" "+str(rpi_time)
                    db_dateTime = str(db_date)+" "+str(db_time)
                    time_sort=[rpi_dateTime,db_dateTime]
                    time_sort.sort()
                    if db_status=='0' and rpi_status=='0':
                        pass
                    elif db_status=='1' and rpi_status=='0':
                        download_template(user_id,template_id)
                    elif db_status=='0' and rpi_status=='1':
                        if time_sort[0]==db_dateTime:
                            dateid = get_dateId(rpi_date)
                            timeid = get_timeId(rpi_time)
                            if not dateid==0 and not timeid==0:
                                upload_template(user_id, template_id,dateid,timeid)
                        else:
                            delete_template(user_id,template_id)
                    elif db_status=='1' and rpi_status=='1':
                        if db_dateTime==rpi_dateTime:
                            pass
                        elif time_sort[0]==db_dateTime:
                            dateid = get_dateId(rpi_date)
                            timeid = get_timeId(rpi_time)
                            if not dateid==0 and not timeid==0:
                                upload_template(user_id, template_id,dateid,timeid)
                        else:
                            download_template(user_id,template_id)
        except Exception as e:
            import traceback
            traceback.print_exc()
	    print('execute error here')
            print e
            print 'just printed error'
            return False
        print('template sync over')
        return True
    except Exception as e:
        print e
        return False

def upload_template(user_id,template_id, dateid, timeid):
    print("uploading template"+str(user_id)+" "+str(template_id))
    print(str(dateid)+" "+str(timeid))
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','rb')
        template = text.read()
        text.close()
        if len(user_id)==16:   
            sql="""update `studentfingerprint` set `template`= %s, `dateID` = %s, `timeID`=%s where `prn`=%s and `templateID`=%s"""
        else:
            sql="""update `facultyfingerprint` set `template`= %s, `dateID` = %s, `timeID`=%s where `facultyid`=%s and `templateID`=%s"""
        try:
            print(sql)
            val = (template,dateid,timeid,user_id,template_id)
            print(val)
            cur.execute(sql,val)
            myconn.commit()
            myconn.close()
            print("Uploaded Successfully")
            return True
        except Exception as e:
            print e
            return False
    except Exception as e:
        print e
        return False

def download_template(user_id, template_id):
    print("downloading template"+str(user_id)+" "+str(template_id))
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        if len(user_id)==16:
            sql="select template, (select datedata.date from datedata where studentfingerprint.dateID = datedata.dateID), (select timedata.time from timedata where studentfingerprint.timeID = timedata.timeID) from studentfingerprint where prn='"+str(user_id)+"' and templateID="+str(template_id)
        else:
            sql="select template, (select datedata.date from datedata where facultyfingerprint.dateID = datedata.dateID), (select timedata.time from timedata where facultyfingerprint.timeID = timedata.timeID) from facultyfingerprint where facultyID="+str(user_id)+" and templateID="+str(template_id)
        try:
            cur.execute(sql)
            result = cur.fetchall()
            for y in result:
                template=y[0]
                text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','w')
                text.write(str(template))
                text.close()
                set_meta_temp_dateTimeStatus(user_id,template_id,y[1],y[2],1)
            myconn.close()
            return True
        except Exception as e:
            print e
            return False
    except Exception as e:
        print e
        return False
            
def delete_template(user_id, template_id):
    try:
        try:
            os.remove('./templates/'+str(user_id)+'-'+str(template_id)+'.txt')
        except Exception as e:
            pass
        meta_template = json.load(open("./docs/meta_template.json"))
        meta_template[str(user_id)+"-"+str(template_id)]="1970-01-01,00:00:00,0"
        with open("./docs/meta_template.json", 'w') as file:
            file.write(json.dumps(meta_template, sort_keys=True))
        return True
    except Exception as e:
        print(e)
        return False

def set_stud_templates(studs):
    id=0
    count = 0
    text = ""
    try:
        print(studs)
        for x in studs:
            template_id=1
            print(x)
            while template_id<3:
                text = ""
                if count==20:
                    count=0
                print count
                while len(text)<count:
                    text=text+"."
                print text
                count=count+1
                printleftline(text,4)
                if set_template(str(x)+"-"+str(template_id),id):
                    set_map_prn(id,x)
                    id = id+1
                template_id=template_id+1
        return True
    except Exception as e:
        print(e)
        return False
    
def set_fac_templates():
    id=199
    count=0
    try:
        with open('./docs/fac-det.txt', "r") as fp:
            print('file opened')
            for x in fp.readlines():
		print x
                x = x.split(",")
                template_id=1
                while template_id<3:
                    text = ""
                    if count==20:
                        count=0
                    print count
                    while len(text)<count:
                        text=text+"."
                    print text
                    count=count+1
                    printleftline(text,4)
                    if set_template(str(x[0])+"-"+str(template_id),id):
                        print set_map_prn(id,x[0])
                        print str(id)+","+str(x[0])
                        id = id-1
                    template_id=template_id+1
        return True
    except Exception as e:
        print(e)
        return False

#---------------Enroll---------------------------------------	

def enroll(user_id,template_id):
    try:
        lcd.clrscr()
        lcd.println("Enroll Start")
        lcd.println("ID :"+str(user_id))
        lcd.println("Template ID :"+str(template_id))
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
            if enroll_main(id):
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
                        today = date.today()
                        time = datetime.datetime.now().strftime("%H:%M:%S")
                        set_meta_temp_dateTimeStatus(user_id,template_id,today,time,1)
                        text = open('./templates/'+str(user_id)+"-"+str(template_id)+'.txt','rb')
                        template = text.read()
                        text.close()
                        dateid = get_dateId(today)
                        timeid = get_timeId(time)
                        print(dateid,timeid)
                        if not dateid==0 and not timeid==0:
                            upload_template(user_id,template_id,dateid,timeid)
                        return True
                    else:
                        lcd.clrscr()
                        lcd.println("Verification")
                        lcd.println("UnSuccessfull")
                        lcd.println("Try Again")
                        sleep(1000)
                        verifyCount=verifyCount+1
                if verifyCount==3:
                    fps.deleteId(id)
                    lcd.clrscr()
                    lcd.println("Verification")
                    lcd.println("Failed")
                    sleep(1000)
                    trialCount=trialCount+1
            else:
                flag=0
            if flag==0:
                return False
        fps.deleteId(id)
    except Exception as e:
        print(e)
        return False

def enroll_main(id):
    try:
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
                fps.deleteId(id)
                sleep(1000)
        return response
    except Exception as e:
        print(e)
        return False

#---------------Utilities---------------------------------------

def get_timeId(time=datetime.datetime.now().strftime("%H:%M:%S")):
    print 'time id function'
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        timeid = 0
        sql="SELECT timeID from timedata where time = '"+str(time)+"'"
        cur.execute(sql)
        result = cur.fetchall()
        for x in result:
            timeid=x[0]
        if timeid==0:
            try:
                sql="insert into timedata values(null,'"+str(time)+"')"
                cur.execute(sql)
                myconn.commit()
                return get_timeId(time)
            except Exception as e:
                print e
                myconn.close()
                return 0
        return timeid
    except Exception as e:
        myconn.close()
        print(e)
        return 0

def get_dateId(date=date.today):
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        dateid = 0
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
            except Exception as e:
                print e
                myconn.close()
                return 0
        return dateid
    except Exception as e:
        myconn.close()
        print(e)
        return 0
    

def get_weekId(week=datetime.datetime.now().isocalendar()[1],year=datetime.datetime.now().year):
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor() 
        weekid = 0
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
                myconn.close()
                return get_weekId(week,year)
            except Exception as e:
                print e
                myconn.close()
                return 0
        return weekid
    except Exception as e:
        myconn.close()
        print(e)
        return 0

def get_class():
    classID = 0
    flag = 0
    while flag==0:
        clrscr()
        println("Select Class")
        println("A - FY")
        println("B - SY")
        println("C - TY")
        key = getKey()
        clrscr()
        if key =='A': 
            println("BCA FY Selected")
            sleep(1000)
            clrscr()
            flag = 1
            classID = 1
        elif key == 'B':
            println("BCA SY Selected")
            sleep(1000)
            clrscr()
            flag = 1
            classID = 2
        elif key == 'C':
            println("BCA TY Selected")
            sleep(1000)
            clrscr()
            flag = 1
            classID = 3
        else:
            println("Invalid Input")
            sleep(1000)
            clrscr()
            flag = 0
    clrscr()
    return classID

def get_roll():
    Roll = "";
    roll = 0
    clrscr()
    printleft("A - Clear")
    printleft("B - Delete")
    printleft("* - Enter")
    while True:
        printleftline("Roll No: " + Roll,4)
        key = getKey()
        if key == 'C' or key == 'D' or key == '#':
            beep(1)
        elif key == 'A':
            Roll = ""
        elif key == 'B':
            if len(Roll) > 0:
                Roll = Roll[0:-1]
            else:
                Roll=""
        elif key == '*':
            roll= int(Roll)
            if 150>roll>0:
                clrscr()
		return roll
            else:
                clrscr()
                println("Invalid Roll Number")
                println("Enter Roll No Again")
                Roll = ""
                roll = 0
                sleep(1500)
		clrscr()
                printleft("A - Clear")
                printleft("B - Delete")
                printleft("* - Enter")
        else:
            Roll = str(Roll) + str(key)

def get_faculty_id():
    facs = []
    try:
        with open('./docs/fac-det.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                facs.append(x[0])
    except Exception as e:
        return False
    print facs
    Roll = "";
    clrscr()
    printleft("A - Clear")
    printleft("B - Delete")
    printleft("* - Enter")
    while True:
        printleftline("Faculty ID : " + Roll,4)
        key = getKey()
        if key == 'C' or key == 'D' or key == '#':
            beep(1)
        elif key == 'A':
            Roll = ""
        elif key == 'B':
            if len(Roll) > 0:
                Roll = Roll[0:-1]
            else:
                Roll=""
        elif key == '*':
            if Roll in facs:
                clrscr()
	        return Roll
            else:
                clrscr()
                println("Invalid Faculty ID")
                println("Facutly Not Found")
                println("with that ID")
                println("Enter ID Again")
                sleep(1500)
		clrscr()
                printleft("A - Clear")
                printleft("B - Delete")
                printleft("* - Enter")
        else:
            Roll = str(Roll) + str(key)

def get_prn():
    studs = []
    try:
        with open('./docs/stud-det.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                x[2] = x[2].replace("\n","")
                studs.append(x[2])
    except Exception as e:
        print e
        return False
    print studs
    Roll = "";
    clrscr()
    printleft("A - Clear")
    printleft("B - Delete")
    printleft("* - Enter")
    while True:
        printleftline("PRN:" + Roll,4)
        key = getKey()
        if key == 'C' or key == 'D' or key == '#':
            beep(1)
        elif key == 'A':
            Roll = ""
        elif key == 'B':
            if len(Roll) > 0:
                Roll = Roll[0:-1]
            else:
                Roll=""
        elif key == '*':
            if Roll in studs:
                clrscr()
	        return Roll
            else:
                clrscr()
                println("Invalid PRN")
                println("Student Not Found")
                println("with that PRN")
                println("Enter PRN Again")
                sleep(1500)
		clrscr()
                printleft("A - Clear")
                printleft("B - Delete")
                printleft("* - Enter")
        else:
            Roll = str(Roll) + str(key)

def insert_attendance(schedule_id,prn):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor()
        timeid=get_timeId(time)
        if not timeid==0:
            sql="insert into `attendance` values(null,'"+str(prn)+"',"+str(schedule_id)+","+str(timeid)+")"    
            cur.execute(sql)
            myconn.commit()
        else:
            file = open('./docs/attendance.txt', "a")
            file.write(str(schedule_id)+","+str(time)+","+str(prn))
            file.close()
            return False
        return True
    except Exception as e:
        if str(e).find('Duplicate entry')==-1:
            file = open('./docs/attendance.txt', "a")
            file.write(str(schedule_id)+","+str(time)+","+str(prn)+"\n")
            file.close()
            return False
        else:
            return True
    except Exception as e:
        return False

def start_lab(schedule_id, faculty_id):
    print 'starting lab'
    time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor()
        print 'define time'
        print 'defined time'
        timeid=get_timeId(time)
        print timeid
        if not timeid==0:
            sql="insert into `facultytimetable` values("+str(schedule_id)+","+str(faculty_id)+")"
            cur.execute(sql)
            myconn.commit()
        else:
            file = open('./docs/attendance.txt', "a")
            file.write(str(schedule_id)+","+str(time)+","+str(faculty_id))
            file.close()
            return False
        return True
    except Exception as e:
        if str(e).find('Duplicate entry')==-1:
            file = open('./docs/attendance.txt', "a")
            file.write(str(schedule_id)+","+str(time)+","+str(faculty_id)+"\n")
            file.close()
            return False
        else:
            return True

def delete_user(user_id):
    try:
        try:
            os.remove('./templates/'+str(user_id)+'-1.txt')
        except Exception as e:
            pass
        try:
            os.remove('./templates/'+str(user_id)+'-2.txt')
        except Exception as e:
            pass
        meta_template = json.load(open("./docs/meta_template.json"))
        meta_template.pop(str(user_id)+"-1", None)
        meta_template.pop(str(user_id)+"-2", None)
        with open("./docs/meta_template.json", 'w') as file:
            file.write(json.dumps(meta_template, sort_keys=True)) 
        return True
    except Exception as e:
        print(e)
        return False

def get_map_prn(id):
    try:
        map = json.load(open("./docs/map.json"))
        user_id = map[str(id)]
        return user_id
    except Exception as e:
        print(e)
        return False

def set_map_prn(id,user_id):
    print('set map'+str(id)+" - "+str(user_id))
    try:
        map = json.load(open("./docs/map.json"))
        map[str(id)]=user_id
        with open("./docs/map.json", 'w') as file:
            file.write(json.dumps(map, sort_keys=True))
        return True
    except Exception as e:
        print(e)
        return False

def clear_map():
    print('clear map')
    try:
        map = json.load(open("./docs/map.json"))
        id = 0;
        while id<200:
            map[str(id)]='0'
            id=id+1
        map[str(200)]='Finger Not Found'
        with open("./docs/map.json", 'w') as file:
            file.write(json.dumps(map, sort_keys=True))
        return True
    except Exception as e:
        print(e)
        return False

def get_meta_temp_dateTimeStatus(template_name):
    try:
        meta_template = json.load(open("./docs/meta_template.json"))
        dateTimeStatus = meta_template[str(template_name)]
        return dateTimeStatus
    except Exception as e:
        print(e)
        return False

def set_meta_temp_dateTimeStatus(user_id,template_id,date,time,status):
    try:
        dateTimeStatus=str(date)+","+str(time)+","+str(status)
        print dateTimeStatus
        meta_template = json.load(open("./docs/meta_template.json"))
        meta_template[str(user_id)+"-"+str(template_id)]=dateTimeStatus
        with open("./docs/meta_template.json", 'w') as file:
            file.write(json.dumps(meta_template, sort_keys=True))
        return True
    except Exception as e:
        print(e)
        return False

def get_fac_name(faculty_id):
    try:
        with open('./docs/fac-det.txt', "r") as fp:
            for x in fp.readlines():
                x = x.split(",")
                print x[0]
                print x[1]
		if x[0]==str(faculty_id):
	            x[1]=x[1].replace("\n","")
		    return x[1]
    except Exception as e:
        print(e)
        return False
 
def get_template(template_name,fps_id):
    try:
        if fps.checkEnrolled(fps_id):
            response=fps.getTemplate(fps_id)
            template=open("./templates/"+str(template_name)+".txt","wb")
            template.write(str(response))
            template.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def set_template(template_name,fps_id):
    try:
        text = open("./templates/"+str(template_name)+".txt","rb")
        template_data = text.read()
        text.close()
        response = fps.setTemplate(fps_id,str(template_data))
        return True
    except Exception as e:
        print(e)
        return False

def println(text):
    length = len(text);
    indent = ((20 - length) / 2);
    i = 0
    while i < indent:
        text = " " + text;
        i=i+1
    i = 0 
    while len(text) < 20:
        text = text + " ";
        i = i+1
    print "lcd :"+str(text)+":"
    lcd.println(text)

def printline(text,line):
    length = len(text);
    indent = ((20 - length) / 2);
    i = 0
    while i < indent:
        text = " " + text;
        i=i+1
    i = 0 
    while len(text) < 20:
        text = text + " ";
        i = i+1
    print "lcd :"+str(text)+":"
    lcd.println(text,line)

def printleft(text):
    print "lcd :"+str(text)+":"
    lcd.println(text)

def printIP():
    ip = socket.gethostbyname(socket.gethostname())
    println(ip)

def printleftline(text,line):
    print "lcd :"+str(text)+":"
    lcd.println(text,line)

def clrscr():
    lcd.clrscr()

def sleep(milsec):
    time.sleep(milsec/1000)

def print_time(line):
    t = time.time()
    rtc.getTime()
    lcd.println(str(rtc.hour)+':'+str(rtc.min)+':'+str(rtc.sec)+' '+str(rtc.date)+'/'+str(rtc.month)+'/'+str(rtc.year),3)

def getKeyPress():
    try:
        for  j in range(4):
            GPIO.output(COL[j],0)
            for i in range(4):
                if GPIO.input(ROW[i])==0:
                    while (GPIO.input(ROW[i])==0):
                        time.sleep(0.2)
                    return MATRIX[i][j]
            GPIO.output(COL[j],1)
        return 'x'
    except Exception as e:
        return 'x'

def getKey():
    try:
        while True:
            for  j in range(4):
                GPIO.output(COL[j],0)
                for i in range(4):
                    if GPIO.input(ROW[i])==0:
                        while (GPIO.input(ROW[i])==0):
                            time.sleep(0.2)
                        return MATRIX[i][j]
                GPIO.output(COL[j],1)
    except Exception as e:
        print(e)
        return False

def check_conn():
    print 'checking connection'
    try:
        myconn = pymysql.connect(host,user,password,database)
        cur = myconn.cursor()
        sql="Select * from class"
        cur.execute(sql)
    except Exception as e:
        print 'connection exception'
        print e
        return False
    return True

#-------------------------Lighting------------------------------------

def beep(sec):
    count = 1
    try:
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
        return True
    except Exception as e:
        print(e)
        return False

def blinkg(sec):
    count = 1
    try:
        while count<=sec:
            GPIO.output(GreenPin,True)
            time.sleep(0.1)
            GPIO.output(GreenPin,False)
            time.sleep(0.1)
            count = count+1
        GPIO.output(GreenPin,False)
        return True
    except Exception as e:
        print(e)
        return False

def blinkr(sec):
    count = 1
    try:
        while count<=sec:
            GPIO.output(RedPin,True)
            time.sleep(0.1)
            GPIO.output(RedPin,False)
            time.sleep(0.1)
            count = count+1
        GPIO.output(RedPin,False)
        return True
    except Exception as e:
        print(e)
        return False

def blinkalt(sec):
    count = 1
    try:
        while count<=sec:
            blinkg(1)
            blinkr(1)
            count = count+1
        return True
    except Exception as e:
        print(e)
        return False
    
def warning(sec):
    count = 1
    try:
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
        return True
    except Exception as e:
        print(e)
        return False

def light_show():
    try:
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
        return True
    except Exception as e:
        print(e)
        return False
