import fingerpi as fp

def Initialize_FPS():
	f = fp.FingerPi()
	response=f.Open(extra_info = True, check_baudrate = True)
	print response

def Terminate_FPS():
		response = f.Close()
		print response
		
Initialize_FPS()
Terminate_FPS()
#CmosLed
#ChangeBaudrate
#GetEnrollCount
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
