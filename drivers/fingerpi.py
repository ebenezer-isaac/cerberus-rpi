import os, sys
import serial
from base import *

class FingerPi():
    def __init__(self, device_id = 0x01,timeout = 2,*args,**kwargs):
        self.port = '/dev/ttyAMA0'
        self.baudrate = 115200
        if not os.path.exists(self.port):
            raise IOError("Port " + self.port + "cannot be opened!")
        self.serial = serial.Serial(
            port = self.port, baudrate = self.baudrate, timeout = timeout,
            *args, **kwargs)
        self.device_id = device_id
        self.timeout = 5
        self.save = False
        self.serial.flushInput()
        self.serial.flushOutput()
    def sendCommand(self, command, parameter = 0x00):
        if type(parameter) == bool:
            parameter = parameter*1
        packet = encode_command_packet(command, parameter, device_id = self.device_id)
        result = len(packet) == self.serial.write(packet)
        self.serial.flush()
        return result
    def getResponse(self, response_len = 12):
        response = self.serial.read(response_len)
        return decode_command_packet(bytearray(response))
    def sendData(self, data, data_len):
        packet = encode_data_packet(data, data_len, device_id = self.device_id)
        result = len(packet) == self.serial.write(packet)
        self.serial.flush()
        return result
    def getData(self, data_len):
        response = self.serial.read(1+1+2+data_len+2)
        return decode_data_packet(bytearray(response))
    def ChangeBaudrate(self, baudrate):
        if self.sendCommand('ChangeBaudrate', baudrate):
            response = self.getResponse()
            self.serial.baudrate = baudrate
        else:
            raise RuntimeError("Couldn't send packet")
    def open(self, extra_info = False, check_baudrate = False):
            # Check baudrate:
         if check_baudrate:
             self.serial.timeout = 0.5
             for baudrate in (self.serial.baudrate,) + self.serial.BAUDRATES:
                 if 9600 <= baudrate <= 115200:
                     self.serial.baudrate = baudrate
                     if not self.sendCommand('Open', extra_info):
                         raise RuntimeError("Couldn't send 'Open' packet!")
                     # print baudrate
                     response = self.getResponse()
                     if response['ACK']:
                         # Decoded something
                         response['Parameter'] = baudrate
                         break
             if  self.serial.baudrate > 115200: # Cannot be more than that
                 raise RuntimeError("Couldn't find appropriate baud rate!")
         else:
             self.sendCommand('Open', extra_info)
             response = self.getResponse()
         data = None
         if extra_info:
             data = self.getData(16+4+4)
         self.serial.timeout = self.timeout
         return [response, data]
    def close (self):
        if self.sendCommand('Close'):
            response = self.getResponse()
            self.serial.flushInput()
            self.serial.flushOutput()
            self.serial.close()
	    response = self.getResponse()
            return response
        else:
            raise RuntimeError("Couldn't send packet")
    def setLED(self, on = False):
        if self.sendCommand('CmosLed', on):
            response = self.getResponse()
	    return response
        else:
            raise RuntimeError("Couldn't send packet")
    def countEnrolled(self):
        if self.sendCommand('GetEnrollCount'):
	    response = self.getResponse()
	    return response
        else:
            raise RuntimeError("Couldn't send packet")
    def checkEnrolled(self, ID):
        if self.sendCommand('CheckEnrolled', ID):
	    response = self.getResponse()
#            if response[0]['Parameter']==0:
#                return True
#	    else:
	    return response
        else:
            raise RuntimeError("Couldn't send packet")
    def isPressFinger(self):
        if self.sendCommand('IsPressFinger'):
            response = self.getResponse()
            if response[0]['Parameter']==0:
		return True
	    else:
		return False 
        else:
            raise RuntimeError("Couldn't send packet")
	def waitForFinger(self):
	    self.setLED(True)
	    while self.isPressFinger()==False:
		pass
            return True
    def deleteId(self, ID):
        if self.sendCommand('DeleteId', ID):
            response = self.getResponse()
            if response[0]['Parameter']==0:
		return True
	    else:
		return False 
        else:
            raise RuntimeError("Couldn't send packet")
    def deleteAll(self):
        if self.sendCommand('DeleteAll'):
            return self.getResponse()[0]['ACK']
        else:
            raise RuntimeError("Couldn't send packet")
    def identify(self):
	self.waitForFinger()
	if self.captureFinger(False):
	    if self.sendCommand('Identify'):
		response = self.getResponse()
	        if response[0]['Parameter']=='NACK_IDENTIFY_FAILED':
		    response[0]['Parameter']='200'
		return response[0]['Parameter']
            else:
		raise RuntimeError("Couldn't send packet")
	else:
	    return 200 
    def captureFinger(self, best_image = False):
        if best_image:
            self.serial.timeout = 10
        if self.sendCommand('CaptureFinger', best_image):
            self.serial.timeout = self.timeout
	    response = [self.getResponse(), None]
	    return response[0]['ACK']
        else:
            raise RuntimeError("Couldn't send packet")
    def getTemplate(self, ID):
        if self.sendCommand('GetTemplate', ID):
            response = self.getResponse()
        else:
            raise RuntimeError("Couldn't send packet")
        self.serial.timeout = None # This is dangerous!
        data = self.getData(498)
        self.serial.timeout = self.timeout
        response = [response, data]
	return response[1]['Data']
    def SetTemplate(self, ID, template):
        if self.sendCommand('SetTemplate', ID):
            response = self.getResponse()
        else:
            raise RuntimeError("Couldn't send packet")
        if self.sendData(template, 498):
            data = self.getResponse()
        else:
            raise RuntimeError("Couldn't send packet (data)")
        response = [response, data]
	return response[1]['Data']
		###########################################
    def EnrollStart(self, ID):
        self.save = ID == -1
        if self.sendCommand('EnrollStart', ID):
            return [self.getResponse(), None]
        else:
            raise RuntimeError("Couldn't send packet")
    def Enroll1(self):
        if self.sendCommand('Enroll1'):
            return [self.getResponse(), None]
        else:
            raise RuntimeError("Couldn't send packet")
    def Enroll2(self):
        if self.sendCommand('Enroll2'):
            return [self.getResponse(), None]
        else:
            raise RuntimeError("Couldn't send packet")
    def Enroll3(self):
        if self.sendCommand('Enroll3'):
            response = self.getResponse()
        else:
            raise RuntimeError("Couldn't send packet")
        data = None
        if self.save:
            data = self.getData(498)
        return [response, data]
