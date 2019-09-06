from driver_fps import *
import mysql.connector
import time
print 'Opening connection... FPS'
Initialize_FPS()
print 'Counting Fingerprints : '
count = CountEnrolled_FPS()
i = 0;
print 'Total number of enrolled fingerprints = '+str(count)
found=0
while (found<count):
	if CheckEnrolled_FPS(i):
		print 'Fingerprint Count '+found+' is at ID '+i
		found = found+1
	i=i+1
print 'Fetching template for id 10'
t = time.time()
data = GetTemplate_FPS(10)
tx_time = time.time() - t
print 'Template Fetched'
print 'Time to transmit:', tx_time
t = time.time()
text = open("template.txt","wb") 
text.write(str(data)) 
text.close()
tx_time = time.time() - t
print 'Template written to .txt file successfully'
print 'Time write to text file:', tx_time
t = time.time()
DeleteId_FPS(10)
tx_time = time.time() - t
print 'Time to delete fingerprint:', tx_time
t = time.time()
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
print 'mysql connection established'
try:
	sql="insert into fingerprints values(%s, %s)"
	val = (2017033800104472)
    cur.execute(sql,val)
except:
    myconn.rollback()
tx_time = time.time() - t
print 'template uploaded to the database file'
print 'Time to upload template:', tx_time
t = time.time()
try:
    cur.execute("select * from fingerprints where prn=201703380010")
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
t = time.time()
text = open("dbtemp.txt","rb") 
template_data = text.read() 
text.close()
tx_time = time.time() - t
print 'Template written to txt file'
print 'Time to  write template to txt file:', tx_time
t = time.time()
response = SetTemplate_FPS(10,template_data)
tx_time = time.time() - t
print 'Template sent to fps'
print 'Time to set the template:', tx_time
print response
count = CountEnrolled_FPS()
i = 0;
print 'Counting Fingerprints : '
print 'Total number of enrolled fingerprints = '+str(count)
found=0
while (found<count):
	if CheckEnrolled_FPS(i):
		print i
		found = found+1
	i=i+1
Terminate_FPS()
print 'Connection closed'

