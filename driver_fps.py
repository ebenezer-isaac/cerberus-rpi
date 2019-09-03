import fingerpi as fp
f = fp.FingerPi()

def Initialize_FPS():
	response =f.Open(extra_info = True, check_baudrate = True)
	f.ChangeBaudrate(115200)
	return response[0]['ACK']
def SetLED_FPS(state):
	response = f.CmosLed(state)
	return response[0]['ACK']
def Terminate_FPS():
	SetLED_FPS(False)
	response = f.Close()
	return response[0]['ACK']
def SetBaudrate_FPS(baud):
	response = f.ChangeBaudrate(int(baud))
	return response[0]['ACK']
def CountEnrolled_FPS():
	response = f.GetEnrollCount()
	return response[0]['Parameter']
def CheckEnrolled_FPS(id):
	response = f.CheckEnrolled(id)
	if response[0]['Parameter']==0:
		return True
	else:
		return False
def IsPressFinger_FPS():
	response = f.IsPressFinger()
	if response[0]['Parameter']==0:
		return True
	else:
		return False
def WaitForFinger_FPS():
	SetLED_FPS(True)
	while IsPressFinger_FPS()==False:
		pass
	return True
def DeleteId_FPS(id):
	response = f.DeleteId(id)
	if response[0]['Parameter']==0:
		return True
	else:
		return False
def Identify_FPS():
	SetLED_FPS(True)
	f.CaptureFinger(False)
	response = f.Identify()
	if response[0]['Parameter']=='NACK_IDENTIFY_FAILED':
		response[0]['Parameter']='200'
	SetLED_FPS(False)
	return response[0]['Parameter']
def GetImage_FPS():
	SetLED_FPS(True)
	f.CaptureFinger(False)
	SetLED_FPS(False)
	response = f.GetImage()
	return response

#Below functions have not been tested

def GetTemplate_FPS(id):
	response = f.GetTemplate(id)
	return response[1]['Data']
def EnrollStart_FPS(id):
	response = f.EnrollStart(id)
	return response[0]['ACK']
def Enroll1_FPS():
	response = f.Close()
	return response[0]['ACK']
def Enroll2_FPS():
	response = f.Close()
	return response[0]['ACK']
def Enroll3_FPS():
	response = f.Close()
	return response[0]['ACK']
def DeleteAll_FPS():
	response = f.Close()
	return response[0]['ACK']
	
#print Initialize_FPS()
#print SetBaudrate_FPS(115200)
#print SetLED_FPS(True)
#print SetLED_FPS(False)
#CountEnrolled_FPS()
#print Terminate_FPS()
