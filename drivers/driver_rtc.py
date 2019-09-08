import datetime
import subprocess

class rtc:
	year = 0
	month = 0
	date = 0
	hour = 0
	min = 0
	sec = 0
	day = ''
	
	def getTime(self):
		timestamp = (str(subprocess.check_output("hwclock -r", shell=True))[:19]).split(' ')
		self.year = int(str(timestamp[0])[:4])
		self.month = int(str(timestamp[0])[5:7])
		self.date = int(str(timestamp[0])[8:10])
		self.hour = int(str(timestamp[1])[0:2])	
		self.min = int(str(timestamp[1])[3:5])
		self.sec = int(str(timestamp[1])[6:8])
		self.day = (datetime.date(self.year, self.month, self.date)).strftime("%a")
		return timestamp[1]+' '+timestamp[0]
	
