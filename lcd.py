import driver_lcd as lcddriver
import subprocess
time = subprocess.check_output("hwclock -r", shell=True)
lcd = lcddriver.lcd()
lcd.println("Hello world")
lcd.println("Ebenezer Isaac")
lcd.println(str(time[:19]))
print time
