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
#sync_all()
#println('Sync Complete')
#sleep(1000)
#clrscr()
#print(delete_all())
#enroll('1','2')
#print_enrolled()
#println("Fac Templates")
#print('setting templates')
#println("Deleting All")
#delete_all()
#println("Done")
#sleep(1000)
#clrscr()
#println("Check Lab")
#print('....'+str(get_fac_name(1))+'....')
"""
while True:
    next_schedule=get_next_schedule()
    if next_schedule==2:
        clrscr()
        print('All Labs for Today are over')
        println("All Labs Over")
        while True:
            pass
    elif next_schedule==3:
        clrscr()
        print('No Labs for today')
        println("No Labs Today")
        while True:
            pass
    elif next_schedule==-1:
        clrscr()
        print('Fatal Error')
        println("Fatal Error")
        println("Sync")
        println("Fatal Error")
        while True:
            pass
    elif next_schedule[0]==0:
        clrscr()
        print('Lab has started')
        println("Lab has started")
        println(str(next_schedule[1][3]))
        println(str(next_schedule[1][4]))
        studs = get_stud_sub_list(next_schedule[1][3],next_schedule[1][4])
        print('students in '+str(next_schedule[1])+" are listed below")
        print(studs)
        sleep(1000)
        clrscr()
        print('setting fingerprints of student who have opted for the subject '+str(next_schedule[1][3])+' of batch '+str(next_schedule[1][4]))
        println("Setting Fac")
        set_fac_templates()
        println("Setting Stud")
        print(set_stud_templates(studs))
        sleep(1000)
        println("Strtng Att")
        #wait for time to start
        clrscr()
        faculty_identification()
        take_attendance()
    elif next_schedule[0]==1:
        print('Lab is going to start')
        studs = get_stud_sub_list(next_schedule[1][3],next_schedule[1][4])
        print('students in '+str(next_schedule[1])+" are listed below")
        print(studs)
	print('setting fingerprints of student who have opted for the subject '+str(next_schedule[1][3])+' of batch '+str(next_schedule[1][4]))
        print(set_stud_templates(studs))
"""
def main_menu():
    clrscr()
    println("Main Menu")
    beep(3)
    clrscr()
    while True:
        clrscr();
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
    while True:
        clrscr();
        printleft("A - ContRegistration");
        printleft("B - SeleRegistration");
        printleft("C - Add Admin");
        printleft("# - Abort");
        key = getKey();
        clrscr();
        if key == 'A':
            clrscr();
            println("Autonomous");
            println("Fingerprint");
            println("Enrollment");
            sleep(1000)
            enroll_cont();
            return
        elif key == 'B':
            clrscr();
            println("Selected PRN");
            println("Fingerprint");
            println("Enrollment");
            sleep(1000)
            enroll_sele();
            return
        elif key == 'C':
            clrscr();
            println("Faculty");
            println("Fingerprint");
            println("Enrollment");
            sleep(1000)
            enroll_sele();
            return
        elif key == '#':
            return
        else:
            println("Invalid Input");
            sleep(1500);
"""
def enroll_cont():
    clrscr();
    printline("A - Cont from Roll");
    printline("B - New Database");
    printline("Any Key to Abort");
    int flag = 0;
    int enrollid = 0;
    int roll = 0;
    int division = 0;
    char key = ' ';
    int limit = 0;
    key = keypad.waitForKey();
    clrscr();
print get_class_studs(2)

    switch (key)
  {
    case 'A':
      flag = 1;
      division = getClass();
      clrscr();
      do
      {
        clrscr();
        printline("Roll No");
        printline("to Continue from");
        delay(2000);
        roll = getRoll();
        enrollid = division * 60;
        if (division == 0)
        {
          if (roll < fyjump || roll >= fyjump + 60)
          {
            clrscr();
            printline("Invalid Roll No");
            printline("Roll !< First Roll)");
            printline("Roll !> Lab Limit)");
            printline("First Roll :" + String(fyjump));
            delay(1500);
            flag = 0;
          }
          else
          {
            enrollid = enrollid + roll - fyjump;
            limit = 59;
          }
        }
        else if (division == 1)
        {
          if (roll < syjump || roll >= syjump + 60)
          {
            clrscr();
            printline("Invalid Roll No");
            printline("Roll !< First Roll)");
            printline("Roll !> Lab Limit)");
            printline("First Roll :" + String(syjump));
            delay(1500);
            flag = 0;
          }
          else
          {
            enrollid = enrollid + roll - syjump;
            limit = 119;
          }
        }
        else if (division == 2)
        {
          if (roll < tyjump || roll >= tyjump + 60)
          {
            clrscr();
            printline("Invalid Roll No");
            printline("Roll !< First Roll)");
            printline("Roll !> Lab Limit)");
            printline("First Roll :" + String(tyjump));
            delay(1500);
            flag = 0;
          }
          else
          {
            enrollid = enrollid + roll - tyjump;
            limit = 179;
          }
        }
      } while (flag != 1);
      break;
    default : flag = 0;
      break;
  }

  if (flag == 1)
  {
    fps.SetLED(true);
    do
    {
      clrscr();
      printline("Roll Number :" + String(roll));
      printline("A- Continue");
      printline("B- Skip    C- Prev");
      printline("Any to Abort");
      char key = ' ';
      key = keypad.waitForKey();
      switch (key)
      {
        case 'A':
          flag = 1;
          break;
        case 'B':
          flag = 2;
          roll++;
          enrollid++;
          break;
        case 'C':
          flag = 2;
          roll--;
          enrollid--;
          break;
        default :
          flag = 0;
          break;
      }
      if (flag == 1)
      {
        if (fps.CheckEnrolled(enrollid))
        {
          clrscr();
          printline("Roll No :" + String(roll));
          printline("Already Enrolled");
          delay(2000);
        }
        else
        {
          clrscr();
          printline("Roll Number :" + String(roll));
          printline("Prss Fingr to Enroll");
          while (fps.IsPressFinger() == false)
          {}
          printline("Reading Finger");
          fps.EnrollStart(enrollid);
          enroll();
          String details = "Enrolled " + String(division) + " " + print3digits(roll);
          writeCLog(details);
          roll++;
          enrollid++;
        }
      }
    } while (flag != 0  && enrollid <= limit );
  }
  if (flag == 0)
  {
    clrscr();
    printline("Exit Cont Registrtn");
    delay(1000);
    clrscr();
  }

def enroll_sele():
    while True:
        clrscr();
        println("Selected PRN")
        println("Enrollment")
        println("Press A to Continue");
        println("Any Key to Abort");
        key = getKey();
        clrscr();
        if key == 'A':
            prn = get_prn();
            id = 1
            while id<3:
                clrscr()
                if check_template_exists(prn,id):
                    println("Fingerprint"+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    enroll(prn,id)
                id = id +1
    else:
        clrscr();
        printline("Exiting");
        sleep(500)
        return

def faculty_enroll():
    while True:
        clrscr();
        println("Selected PRN")
        println("Enrollment")
        println("Press A to Continue");
        println("Any Key to Abort");
        key = getKey();
        clrscr();
        if key == 'A':
            faculty_id = get_faculty_id();
            id = 1
            while id<3:
                clrscr()
                if check_template_exists(prn,id):
                    println("Fingerprint"+str(id))
                    println("Already")
                    println("Exists")
                    sleep(1000)
                else:
                    enroll(prn,id)
                id = id +1
    else:
        clrscr();
        printline("Exiting");
        sleep(500)
        return
"""
pass
main_menu()
#print 'outside while loop'
#sync_class()
#print start_lab(253,1)
#print insert_attendance(253,'2017033800104747')
#get_roll()
auth_result  = authorization()
print auth_result
if not auth_result:
    clrscr()
    println("Canceled")
else:
    clrscr()
    println("Authorized")
    println("Proceeding")
    sleep(1000)
    print auth[1]

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

