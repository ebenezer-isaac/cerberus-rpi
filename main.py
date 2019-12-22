#Intial Setup
#Enable SPI, I2C
#Disable Serial Shell, Enable Serial Hardware from raspi-config
#apt-get -y install python-pip python-mysql.connector python-smbus wiringPi
#sudo apt-get install python-rpi.gpio python3-rpi.gpio
#pip install mysql-python pyserial RPi.GPIO wiringPi gpio
#echo "dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait" > /boot/cmdline.txt
#sudo systemctl mask serial-getty@ttyAMA0.
#gpio mode 15 ALT0 gpio mode 16 ALT0
#sudo apt-get install python3-mysql.connector
#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot python /home/pi/cerberus-rpi/boot.py >/home/pi/bootlog/cronlog 2>&1' at the end of the file
from functions import *
println('Project Cerberus')
println('The')
println('Attndance Initiative')
setup()
sleep(500)
sync_all()
print(delete_all())
while True:
    next_schedule=get_next_schedule()
    if next_schedule==2:
        clrscr()
        println("All Labs Over")
        while True:
            pass
    elif next_schedule==3:
        clrscr()
        println("No Labs Today")
        while True:
            pass
    elif next_schedule==-1:
        clrscr()
        println("Fatal Error")
        println("Timetable:Error")
        println("Restart to")
        println("Try Again")
        while True:
            pass
    elif next_schedule[0]==0:
        clrscr()
        println("Lab has started")
        println(str(next_schedule[1][3]))
        println(str(next_schedule[1][4]))
        studs = get_stud_sub_list(next_schedule[1][3],next_schedule[1][4])
        sleep(1000)
        clrscr()
        delete_all()
        set_fac_templates()
        set_stud_templates(studs)
        auth_result  = authorization(next_schedule[0])
        while not auth_result:
            clrscr()
            println("Canceled")
            sleep(1000)
        else:
            clrscr()
            println(str(auth_result[2]))
            println("Authorized")
            println("<<>>")
            println("Lab Started")
            sleep(1000)
            take_attendance()
    elif next_schedule[0]==1:
        #wait for lab to start
def main_menu():
    clrscr()
    println("Main Menu")
    clrscr()
    while True:
        clrscr()
        printleft("A- Check Connection")
        printleft("B- Sync Now")
        printleft("C- Enroll")
        printleft("#- Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            println("Check Connection")
            printIP()
            if check_conn():
                println("Connection")
                println("Available")
                sleep(1500)
            else:
                clrscr()
                println("Connection")
                println("Unavailable")
                printIP()
                println("Press Any Key")
                key = getKey()
        elif key == 'B':
            sync_all()
        elif key == 'C':
            println("Enroll Fingerprint")
            sleep(1000)
            enroll_menu()
            return
        elif key == '#':
            return
        else:
            println("Invalid Input")
            sleep(1500)

def enroll_menu():
    delete_all()
    while True:
        clrscr()
        printleft("A - ContRegistration")
        printleft("B - SeleRegistration")
        printleft("C - Add Admin")
        printleft("# - Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            enroll_cont()
            return
        elif key == 'B':
            enroll_sele()
            return
        elif key == 'C':
            faculty_enroll()
            return
        elif key == '#':
            return
        else:
            println("Invalid Input")
            sleep(1500)

def enroll_cont():
    clrscr()
    println("Autonomous")
    println("Enrollment")
    println("A to Continue")
    println("Any Key to Abort")
    key = getKey()
    clrscr()
    if key == 'A':
        classID = get_class()
        studs = get_class_studs(classID)
        index = 0
        while index < len(studs):
            clrscr()
            println("Roll Number :" + str(studs[index][1]))
            println("A- Continue")
            println("B- Skip    C- Prev")
            println("Any to Abort")
            key = getKey()
            if key == 'A':
                id = 1
                while id<3:
                    clrscr()
                    if check_template(prn,id):
                        println("Fingerprint "+str(id))
                        println("Already")
                        println("Exists")
                        sleep(1000)
                    else:
                        clrscr()
                        println("PRN:"+str(prn))
                        println("Fingerprint "+str(id))
                        println("Press A to Continue")
                        println("Any Key to Skip")
                        key = getKey()
                        if key == 'A':
	                    enroll(studs[index][0],id)
                    id = id +1
            elif key == 'B':
                pass
            elif key == 'C':
                if not index==0:
                    index = index -2
            else:
                clrscr()
                println("Exiting")
                sleep(500)
                return
            index = index+1
        clrscr()
        println("All Students Over")  
        sleep(1000)
    else:
        clrscr()
        println("Exiting")
        sleep(500)
        return

def enroll_sele():
    while True:
        clrscr()
        println("Selected PRN")
        println("Enrollment")
        println("Press A to Continue")
        println("Any Key to Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            prn = get_prn()
            id = 1
            while id<3:
                clrscr()
                if check_template(prn,id):
                    println("Fingerprint "+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    clrscr()
                    println("PRN:"+str(prn))
                    println("Fingerprint "+str(id))
                    println("Press A to Continue")
                    println("Any Key to Skip")
                    key = getKey()
                    if key == 'A':
                        enroll(prn,id)
                id = id +1
        else:
            clrscr()
            println("Exiting")
            sleep(500)
            return

def faculty_enroll():
    while True:
        clrscr()
        println("Faculty")
        println("Enrollment")
        println("Press A to Continue")
        println("Any Key to Abort")
        key = getKey()
        clrscr()
        if key == 'A':
            faculty_id = get_faculty_id()
            id = 1
            while id<3:
                clrscr()
                if check_template(faculty_id,id):
                    println("Fingerprint"+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    enroll(faculty_id,id)
                id = id +1
    else:
        clrscr()
        printline("Exiting")
        sleep(500)
        return
main_menu()
#print 'outside while loop'
#sync_class()
#print start_lab(253,1)
#print insert_attendance(253,'2017033800104747')
#get_roll()

def take_attendance():
    id = 0
    while True:
        clrscr()
        println("Taking")
        println("Attendance")
        println("Press Finger")
        id = identify()
        clrscr()
        if id==200:
             println("Not")
             println("Found")
             println("Try Again")
        else:
             println(str(id))
             println("Found")
             println("Send to DB")
        println("Waiting 1 sec")
        sleep(1000)

print 'show has ended'

