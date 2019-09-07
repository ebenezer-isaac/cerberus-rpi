from driver_fps import *
import subprocess
import mysql.connector
print 'Opening connection...'
Initialize_FPS()
id = 0
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
while id<=199:
	if CheckEnrolled_FPS(id):
		data = GetTemplate_FPS(id)
		text = open("./templates/template-id-"+str(id)+".txt","w") 
		text.write(str(data)) 
		text.close()
		print 'Template Fetched for id '+str(id)
		try:
			sql="""insert into fingerprints values(%s, %s)"""
			val = (id,data)
			cur.execute(sql,val)
		except:
			myconn.rollback()
		print 'Template Uploaded for id '+str(id)
	id = id+1
DeleteAll_FPS()
Terminate_FPS()
print 'Connection closed'
print 'Templates stored in templates folder successfully'
