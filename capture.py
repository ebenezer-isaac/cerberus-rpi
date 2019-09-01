import fingerpi as fp
import time
import pickle

print 'Opening connection...'
f = fp.FingerPi()
f.Open(extra_info = True, check_baudrate = True)
f.ChangeBaudrate(115200)
f.CmosLed(True)
print 'Place the finger on the scanner to capture finger'
fingerflag=f.IsPressFinger()[0]["Parameter"]
while fingerflag!="""True""":
	if fingerflag != '4114':
		print 'Unknown Error occured', fingerflag
	fingerflag=f.IsPressFinger()[0]["Parameter"]
capture = f.CaptureFinger()
if capture[0]['ACK']:
	print 'Image has been captured'
	print 'Fetching image'
	raw_img = f.GetImage()
	print 'Image Fetched'
	f.CmosLed(False)
	f.Close()
	print 'Closing connection...'
	with open('capture.pickle', 'wb') as f:
		pickle.dump(raw_img, f)


