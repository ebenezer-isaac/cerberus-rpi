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
            time = x[2]
            comments = x[3]
            print ('(\''+str(date)+' '+str(time)+'\','+str(comments)+')')
            #prn = comments[0]
            #status = comments[1]
	except:
		myconn.rollback()
    """    
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