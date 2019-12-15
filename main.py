#Intial Setup
#Enable SPI, I2C
#Disable Serial Shell, Enable Serial Hardware from raspi-config
#apt-get -y install python-pip python-mysql.connector python-smbus wiringPi
#sudo apt-get install python-rpi.gpio python3-rpi.gpio
#pip install mysql-python pyserial RPi.GPIO wiringPi gpio
#echo "dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait" > /boot/cmdline.txt
#sudo systemctl mask serial-getty@ttyAMA0.service
#gpio mode 15 ALT0; gpio mode 16 ALT0
#sudo apt-get install python3-mysql.connector
#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot python /home/pi/cerberus-rpi/boot.py >/home/pi/bootlog/cronlog 2>&1' at the end of the file

from functions import *
println('Project Cerberus')
println('The')
println('Attndance Initiative')
setup()
println('Syncing Files')
sync_all()
clrscr()
println('Sync Complete')
sleep(1000)
#println(get_next_scheduleId())
#sleep(1000)
#print('sleep finished')
#id = 0
#print_enrolled()
#print('getting fingerprint')
#print(get_template("backup-"+str(id),id))
#print('deleting fingerprint')
#print(delete_fingerprint(id))
#print('setting fingerprint')
#print(set_template("backup-"+str(id),181))
#print_enrolled()
#print('identify fingerprint')
#print(backup_templates())
#print(delete_all())
#id = 2
#name = 'Ebenezer Isaac'
#response = enroll(id)
#if response:
#    clrscr()
#    println("Enroll Successfull")
#    set_map_prn(id,name)
#    sleep(1000)
#else:
#    clrscr()
#    println("Enroll Unsuccessfull")
#    sleep(1000)
#print("Enter Key")
#print(getKey())
#studs=get_stud_sub_list('BCA1538',2)
#set_templates(studs)
#delete_all()
#enroll('2017033800104472','1')
#get_template('2017033800104472-1',0)
#upload_template('2017033800104472','1')
#download_template('2017033800104472','1')
next_schedule=get_next_schedule()
print(next_schedule)
if next_schedule==2:
    print('All Labs for Today are over')
elif next_schedule==3:
    print('No Labs for today')
elif next_schedule[0]==0:
    print('Lab has started')
    print(get_stud_sub_list(next_schedule[1][3],next_schedule[1][4]))
elif next_schedule[0]==1:
    print('Lab is going to start')
    print(get_stud_sub_list(next_schedule[1][3],next_schedule[1][4]))
print 'show has ended'
while True:
    clrscr()
    println('Identify Finger')
    println("Press Finger")
    response = identify()
    clrscr()
    println(response)
    println("Waiting 1 sec")
    sleep(1000)

