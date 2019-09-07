from driver_fps import *
import mysql.connector
print 'Open FPS'
Initialize_FPS()
SetLED_FPS(True)
DeleteAll_FPS()
print 'Press Finger'
WaitForFinger_FPS()
t = time.time()
CaptureFinger_FPS()
id = 200
prn = 0
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
try:
cur.execute("select * from fingerprints")
result = cur.fetchall()
for x in result:
	if id==200:
		data=x[1]
		response = SetTemplate_FPS(0,str(data))
		if str(response[0]['ACK']:
			print 'successfull template set        : '+str(count)+
		else:
			print 'error in setting template number: '+str(count)
		id = Identify_FPS()
		if id==0:
			prn = x[0]
		DeleteId_FPS(0)
except:
	myconn.rollback()
myconn.close()
tx_time = time.time() - t
print 'PRN : '+str(prn)
print 'Time taken:', tx_time
Terminate_FPS()