import datetime
import subprocess

class RTC:
	year = 0
	month = 0
	date = 0
	hour = 0
	min = 0
	sec = 0
	day = ''
	def getTime(self):
		timestamp = (str(subprocess.check_output("hwclock", shell=True))[:19]).split(' ')
		self.year = str(timestamp[0][:4])
		self.month = "{:02d}".format(int(str(timestamp[0])[5:7]))
		self.date = "{:02d}".format(int(str(timestamp[0])[8:10]))
		self.hour = "{:02d}".format(int(str(timestamp[1])[0:2]))
		self.min = "{:02d}".format(int(str(timestamp[1])[3:5]))
		self.sec = "{:02d}".format(int(str(timestamp[1])[6:8]))
		self.day = (datetime.date(int(self.year), int(self.month), int(self.date))).strftime("%a")
		return self.year+'/'+self.month+'/'+self.date+' '+self.hour+':'+self.min+':'+self.sec
