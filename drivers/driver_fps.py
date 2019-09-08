import fingerpi as fp

class fps:
	self.f = fp.FingerPi()
	def Initialize(self):
		response =f.Open(extra_info = True, check_baudrate = True)
		f.ChangeBaudrate(115200)
		return response[0]['ACK']
	def Terminate(self):	
		SetLED(False)
		response = f.Close()
		return response[0]['ACK']
	def SetLED(selfstate):
		response = f.CmosLed(state)
		return response[0]['ACK']
	def CountEnrolled(self):
		response = f.GetEnrollCount()
		return response[0]['Parameter']
	def CheckEnrolled(self, id):
		response = f.CheckEnrolled(id)
		if response[0]['Parameter']==0:
			return True
		else:
			return False
	def IsPressFinger(self):
		response = f.IsPressFinger()
		if response[0]['Parameter']==0:
			return True
		else:
			return False
	def WaitForFinger(self):
		SetLED(True)
		while IsPressFinger()==False:
			pass
		return True
	def DeleteId(self, id):
		response = f.DeleteId(id)
		if response[0]['Parameter']==0:
			return True
			else:
			return False
	def Identify(self):
		SetLED(True)
		f.CaptureFinger(False)
		SetLED(False)
		response = f.Identify()
		if response[0]['Parameter']=='NACK_IDENTIFY_FAILED':
			response[0]['Parameter']='200'
		return response[0]['Parameter']
		#return response[0]['Parameter']
	def GetTemplate(self, id):
		response = f.GetTemplate(id)
		return response[1]['Data']
	def SetTemplate(self, id,data):
		response = f.SetTemplate(id,data)
		return response
	def EnrollStart(self, id):
		response = f.EnrollStart(id)
		return response[0]['ACK']
	def Enroll1(self):
		response = f.Enroll1()
		return response[0]['ACK']
	def Enroll2(self):
		response = f.Enroll2()
		return response[0]['ACK']
	def Enroll3(self):
		response = f.Enroll3()
		return response[0]['ACK']
	def DeleteAll(self):
		response = f.DeleteAll()
		return response[0]['ACK']