#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot sh /home/pi/cerberus-rpi/launcher.sh >/home/pi/bootlog/cronlog 2>&1' at the end of the file

l = [('2017/09/10 13:19:38', 'employee_id', 'enrolled'),
('2017/09/10 12:15:21', 'employee_id', 'deleted'),
('2017/09/10 21:19:34', 'employee_id', 'enrolled'),
('2017/09/10 22:42:50', 'employee_id', 'deleted'),
('2017/09/10 16:53:03', 'employee_id', 'enrolled')]
print list.sort()