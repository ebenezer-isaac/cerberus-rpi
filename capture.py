import fingerpi as fp
import time
import pickle

print 'Opening connection...'
f = fp.FingerPi()
f.Open(extra_info = True, check_baudrate = True)
f.ChangeBaudrate(115200)
print 'Place the finger on the scanner to capture finger'
f.CmosLed(True)
if f.IsPressFinger()[0]["Parameter"]=="""True""":
	response = f.CaptureFinger()
	if response[0]['ACK']:
		print 'Image has been captured'
		print 'Fetching image'
		raw_img = f.GetImage()
		print 'Image Fetched'
		f.CmosLed(False)
		f.Close()
		print 'Closing connection...'
		with open('capture.pickle', 'wb') as f:
			pickle.dump(raw_img, f)
	if response[0]['Parameter'] != 'NACK_FINGER_IS_NOT_PRESSED':
		print 'Unknown Error occured', response[0]['Parameter']
f.CmosLed(False)

