import RPi.GPIO as GPIO
import time
class KPD:
	GPIO.setmode(GPIO.BCM)
	MATRIX = [
	[1,2,3,'A'],
	[4,5,6,'B'],
	[7,8,9,'C'],
	['*',0,'#','D']	
	]
	COL = [12,26,13,6]
	ROW = [5,22,27,17]
	def __init__(self):
		for j in range(4):
			GPIO.setup(COL[j], GPIO.OUT)
			GPIO.output(COL[j],1)
		for i in range(4):
			GPIO.setup(ROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)
   
	def getChar(self):
		key = ''
		while key == '':
			for  j in range(4):
				GPIO.output(COL[j],0)
				for i in range(4):
					if GPIO.input(ROW[i])==0:
						key = MATRIX[i][j]
						while (GPIO.input(ROW[i])==0):
							time.sleep(0.2)
						return key
				GPIO.output(COL[j],1)