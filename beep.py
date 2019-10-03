import RPi.GPIO as GPIO
LedPin1 = 36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LedPin1, GPIO.OUT)
GPIO.output(LedPin1,False)

