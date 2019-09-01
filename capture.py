import fingerpi as fp
import pickle

print 'Opening connection...'
f = fp.FingerPi()
f.Open(extra_info = True, check_baudrate = True)
f.ChangeBaudrate(115200)
f.CmosLed(True)
print 'Place the finger on the scanner to capture finger'
fingerflag=f.IsPressFinger()[0]["Parameter"]
while fingerflag==4114:
	fingerflag=f.IsPressFinger()[0]["Parameter"]
capture = f.CaptureFinger()
f.CmosLed(False)
if capture[0]['ACK']:
	print 'Image has been captured'
	print 'Fetching image'
	raw_img = f.GetImage()
	print 'Image Fetched'
	f.Close()
	print 'Closing connection...'
	with open('capture.pickle', 'wb') as f:
		pickle.dump(raw_img, f)