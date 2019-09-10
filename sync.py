import mysql.connector
import time
import os
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
	id = sync[x][1]
	status = sync[x][2]
	source = sync[x][3]
	if source=='rpi'
	if status=='delete':
                os.remove("/templates/"+str(prn))
            elif status=='enroll':
                try:
                    sql=select * from `fingerprints` where prn=%s
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
sync()
