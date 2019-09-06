from driver_fps import *
import subprocess
print 'Opening connection...'
Initialize_FPS()
id = 0
while id<=199:
	if CheckEnrolled_FPS(id):
		data = GetTemplate_FPS(id)
		text = open("./templates/template-id-"+str(id)+".txt","w") 
		text.write(str(data)) 
		text.close()
		print 'Template Fetched for id '+str(id)
	id = id+1
Terminate_FPS()
print 'Connection closed'
print 'Templates stored in templates folder successfully'
