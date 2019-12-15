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
#print(delete_all())
#enroll('2017033800104472','1')
def attendance():
    next_schedule=get_next_schedule()
    if next_schedule==2:
        print('All Labs for Today are over')
    elif next_schedule==3:
        print('No Labs for today')
    elif next_schedule==-1:
        print('Fatal Error')
    elif next_schedule[0]==0:
        print('Lab has started')
        print(get_stud_sub_list(next_schedule[1][3],next_schedule[1][4]))
    elif next_schedule[0]==1:
        print('Lab is going to start')
        print(get_stud_sub_list(next_schedule[1][3],next_schedule[1][4]))
attendance()
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

