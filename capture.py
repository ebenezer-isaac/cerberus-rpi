from fingerprint import *
import pickle

print 'Opening connection...'
Initialize_FPS()
SetLED_FPS(True)
print 'Place the finger on the scanner to capture finger'
WaitForFinger_FPS()
print 'Fetching image'
image = GetImage_FPS()
print 'Image Fetched'
Terminate_FPS()
print 'Connection closed'
with open('capture.pickle', 'wb') as f:
	pickle.dump(image, f)
print 'Image written to .pickle file successfully'
text = open("capture.txt","w") 
text.write(str(image)) 
text.close()
print 'Image written to .txt file successfully'
