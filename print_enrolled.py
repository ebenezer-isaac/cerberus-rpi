from driver_fps import *
Initialize_FPS()
count = CountEnrolled_FPS()
i = 0;
print 'Total number of enrolled fingerprints = '+str(count)
found=0
while (found<count):
	if CheckEnrolled_FPS(i):
		print 'Fingerprint Count '+found+' is at ID '+i
		found = found+1
	i=i+1
Terminate_FPS()
