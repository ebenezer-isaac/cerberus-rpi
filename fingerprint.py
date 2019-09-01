import fingerpi as fp
f = fp.FingerPi()

def Initialize_FPS():
	response =f.Open(extra_info = True, check_baudrate = True)
	return response[0]['ACK']
def SetLED_FPS(state):
	response = f.CmosLed(state)
	return response[0]['ACK']
def Terminate_FPS():
	response = f.Close()
	return response[0]['ACK']
def SetBaudrate_FPS(baud):
	response = f.ChangeBaudrate(int(baud))
	return response[0]['ACK']
def CountEnrolled_FPS():
	print f.GetEnrollCount()
print Initialize_FPS()
print SetBaudrate_FPS(115200)
print SetLED_FPS(True)
print SetLED_FPS(False)
CountEnrolled_FPS()
print Terminate_FPS()
#CheckEnrolled
#EnrollStart
#Enroll1
#Enroll2
#Enroll3
#IsPressFinger
#DeleteId
#DeleteAll
#Identify
#VerifyTemplate
#IdentifyTemplate
#CaptureFinger
#MakeTemplate
#GetImage
#GetRawImage
#GetTemplate
