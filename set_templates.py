from driver_fps import *
import subprocess
import mysql.connector
print 'Opening connection...'
Initialize_FPS()
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
DeleteAll_FPS()
try:
	cur.execute("select * from fingerprints")
	result = cur.fetchall()
	for x in result:
		id=x[0]
		data = x[1]
		print id
		print 'Template Fetched for id '+str(id)
		text = open("./templates/template-id-"+str(id)+".txt","w") 
		text.write(str(data)) 
		text.close()
		print 'Template Written for id '+str(id)
		response = SetTemplate_FPS(id,str(data));
		print response
except mysql.connector.Error as err:
	print("Something went wrong: {}".format(err))
Terminate_FPS()
print 'Connection closed'
print 'Templates stored in templates folder successfully'


