from driver_fps import *
import pickle

print 'Opening connection...'
Initialize_FPS()
SetLED_FPS(True)
data = GetTemplate_FPS(180)
print 'Template Fetched'
Terminate_FPS()
print 'Connection closed'
with open('template.pickle', 'w') as f:
	pickle.dump(data, f)
print 'Template written to .pickle file successfully'
text = open("template.txt","w") 
text.write(str(data)) 
text.close()
print 'Template written to .txt file successfully'
