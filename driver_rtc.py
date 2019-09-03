#2019-09-04 00:10:02.891271+05:30
def GetTime_rtc():
	timestamp = (str(subprocess.check_output("hwclock -r", shell=True))[:19]).split(' ')
	year = str(timestamp[0])[:4]
	month = str(timestamp[0])[5:7]
	date = str(timestamp[0])[8:10]
	hour = str(timestamp[1])[0:2]
	min = str(timestamp[1])[3:5]
	sec = str(timestamp[1])[6:8]
	