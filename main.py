#Intial Setup Enable SPI, I2C Disable Serial Shell, Enable Serial 
#Hardware from raspi-config apt-get -y install python-pip 
#python-mysql.connector python-smbus wiringPi sudo apt-get install 
#python-rpi.gpio python3-rpi.gpio pip install mysql-python pyserial 
#RPi.GPIO wiringPi gpio echo "dwc_otg.lpm_enable=0 console=tty1 
#root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait" > 
#/boot/cmdline.txt sudo systemctl mask serial-getty@ttyAMA0. gpio mode 
#15 ALT0 gpio mode 16 ALT0 sudo apt-get install python3-mysql.connector 
#To run this python script on startup (ignore quotes) Run 'crontab -e' 
#Paste '@reboot python /home/pi/cerberus-rpi/boot.py 
#>/home/pi/bootlog/cronlog 2>&1' at the end of the file
import datetime
from functions import *
println('Project Cerberus')
println('The')
println('Attndance Initiative')
setup()
sleep(500)
clrscr()
sync_all()
#upload_template('2019033800135534','1',14,6)
#upload_template('2019033800135534','2',14,6)
#enroll('2019033800100921','1')
"""println("Setting")
println("Up")
println("Faculty")
println("Fingerprints")
delete_all()
set_fac_templates()

try:
    while True:
        sync_all()
        print 'sync over'
 	next_schedule=get_next_schedule()
 	print next_schedule
        if next_schedule==2:
	    clrscr()
	    println("All Labs Over")
	    println("Power Off")
	    println("Device")
	    println("# for Menu")
	    key = getKey()
            if key=='#':
                main_menu()
        elif next_schedule==3:
	    clrscr()
	    println("No Labs Today")
	    println("Power Off")
	    println("Device")
	    println("# for Menu")
            key = getKey()
            if key=='#':
                main_menu()
	elif next_schedule==-1:
	    clrscr()
	    println("Fatal Error")
	    println("Timetable:Error")
	    println("Restart: Try Again")
	    println("# for Menu")
            key = getKey()
            if key=='#':
                main_menu()
	elif next_schedule[0]==0:
	    clrscr()
	    println("Lab has started")
	    println(str(next_schedule[1][5]))
	    println("Batch :"+str(next_schedule[1][4]))
	    studs = get_stud_sub_list(next_schedule[1][3],next_schedule[1][4])
	    sleep(1000)
            clrscr()
	    println("Setting")
	    println("Up")
	    println("Fingerprints")
	    delete_all()
	    set_fac_templates()
	    set_stud_templates(studs)
	    auth_result  = authorization(next_schedule[1][0])
            print 'back in main'
            print auth_result
	    while not auth_result:
	    	clrscr()
	 	println("Canceled")
		sleep(1000)
	        auth_result  = authorization(next_schedule[1][0])
	    clrscr()
	    println(str(auth_result[2]))
	    println("Authorized")
	    println("<<>>")
	    println("Lab Started")
	    sleep(1000)
	    take_attendance(next_schedule[1][0],next_schedule[1][2],next_schedule[1][5], next_schedule[1][4])
        elif next_schedule[0]==1:
            clrscr()
            println("Lab will Start") 
            println(str(next_schedule[1][1]))
            println("Subject:")
            println(str(next_schedule[1][5]))
            while datetime.datetime.now().strftime("%H:%M:%S")<next_schedule[1][1]:
                key = getKeyPress()
                if key=='#':
                    print 'key pressed'
                    main_menu()
                    print 'inside main py'
except Exception as e:
    print(e)
print 'show has ended'

"""
