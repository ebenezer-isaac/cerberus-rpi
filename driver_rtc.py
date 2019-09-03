#2019-09-04 00:10:02.891271+05:30
#timestamp = (str("2019-09-04 00:10:02.891271+05:30")[:19]).split(' ')
import datetime

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
		self.year = str(timestamp[0])[:4]
		self.month = str(timestamp[0])[5:7]
		self.date = str(timestamp[0])[8:10]
		self.hour = str(timestamp[1])[0:2]	
		self.min = str(timestamp[1])[3:5]
		self.sec = str(timestamp[1])[6:8]
		self.day = (datetime.date(year, month, date)).strftime("%a")
		return timestamp[1]+' '+timestamp[0]
	