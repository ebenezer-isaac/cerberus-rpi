#To run this python script on startup (ignore quotes)
#Run 'crontab -e'
#Paste '@reboot python /home/pi/cerberus-rpi/boot.py >/home/pi/bootlog/cronlog 2>&1' at the end of the file
import functions
println("Boot Complete")
println("Getting Ready")
setup()
enroll(5)
while True:
    clrscr()
    println("Press Finger")
    id = fps.identify()
    if int(id)==200:
	clrscr()
        println("Finger not found")
	#lcd.println("Light Show")
	#beep(2)
	time.sleep(1)
	#light_show()
    else:
        prn = get_prn(id)
        clrscr()
        println("PRN:"+str(prn))
        println("Wait 1 Second")
        time.sleep(1)
