from driver_fps import *
import pickle
print 'Opening connection...'
Initialize_FPS()
data = GetTemplate_FPS(10)
print 'Template Fetched'
Terminate_FPS()
print 'Connection closed'
text = open("template.txt","w") 
text.write(str(data)) 
text.close()
print 'Template written to .txt file successfully'
