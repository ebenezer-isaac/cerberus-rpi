from driver_fps import *
import pickle

print 'Opening connection...'
Initialize_FPS()
SetLED_FPS(True)
text = open("dbtemp.txt","rb") 
template_data = text.read() 
text.close()
response = SetTemplate_FPS(10,template_data)
print response
Terminate_FPS()
print 'Connection closed'
print 'Template has been set in the scanner'
