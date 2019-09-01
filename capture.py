import * from fingerprint
import pickle

print 'Opening connection...'
Initialize_FPS()
SetLED_FPS(True)
print 'Place the finger on the scanner to capture finger'
while !IsPressFinger_FPS():
	pass
print 'Fetching image'
image = GetImage_FPS()
print 'Image Fetched'
Terminate_FPS()
print 'Connection closed'
with open('capture.pickle', 'wb') as f:
	pickle.dump(raw_img, f)
print 'Image written to .pickle file successfully'
