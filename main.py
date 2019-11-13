#Intial Setup
#Enable SPI, I2C
#Disable Serial Shell, Enable Serial Hardware from raspi-config
#apt-get -y install python-pip python-mysql.connector python-smbus wiringPi
#pip install mysql-python pyserial RPi.GPIO wiringPi gpio
#echo "dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait" > /boot/cmdline.txt
#sudo systemctl mask serial-getty@ttyAMA0.service
#gpio mode 15 ALT0; gpio mode 16 ALT0

#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot python /home/pi/cerberus-rpi/boot.py >/home/pi/bootlog/cronlog 2>&1' at the end of the file

from functions import *
println('Project Cerberus')
println('The')
println('Attndance Initiative')
setup()
sleep(1)
id = 23
name = 'Meghna Maam 2'
response = enroll(id)
if response:
    clrscr()
    println("Enroll Successfull")
    set_map_prn(id,name)
    sleep(1000)
else:
    clrscr()
    println("Enroll Unsuccessfull")
    sleep(1000)
while True:
    clrscr()
    println('Identify Finger')
    println("Press Finger")
    response = identify()
    clrscr()
    println(response)
    println("Waiting 1 sec")
    sleep(1000)
