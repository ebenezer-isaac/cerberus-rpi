from driver_fps import *
import mysql.connector
import time
print 'Open FPS'
Initialize_FPS()
SetLED_FPS(True)
DeleteAll_FPS()
print 'Press Finger'
WaitForFinger_FPS()
t = time.time()
CaptureFinger_FPS()
prn=200
count=0
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
try:
	cur.execute("select * from fingerprints")
	result = cur.fetchall()
	for x in result:
		DeleteId_FPS(x[0])
		data=x[1]
		response = SetTemplate_FPS(x[0],str(data))
		if response[0]['ACK']:
			print 'successfull template set        : '+str(x[0])
		else:
			print 'error in setting template number: '+str(x[0])
		id = Identify_FPS()
		print id
		if id==0:
			prn = x[0]
		if x[0]==5:
			print 'waiting'
			WaitForFinger_FPS()
			print CapIdentify_FPS()
except mysql.connector.Error as err:
	print("Something went wrong: {}".format(err))
	myconn.close()
tx_time = time.time() - t
print 'PRN : '+str(prn)
print 'Time taken:', tx_time
Terminate_FPS()
