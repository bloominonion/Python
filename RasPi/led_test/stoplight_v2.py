import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def Main():
    try:
        while True:
            LightsOff()
            InputState = GPIO.input(22)
            if InputState == False:
                print('Button pressed')
                Blinker()
                time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup

def Blinker():
    count = 0
    blinks = 1
    sleep = 0.5
    while (count<blinks):
        LightGrn()
        time.sleep(sleep*5)
        LightYlw()
        time.sleep(sleep)
        LightRed()
        time.sleep(sleep*3)
        count = count + 1

def LightsOff():
    GPIO.output(19,GPIO.LOW)
    GPIO.output(6,GPIO.LOW)
    GPIO.output(17,GPIO.LOW)

def LightRed():
    LightsOff()
    GPIO.output(17,GPIO.HIGH)

def LightYlw():
    LightsOff()
    GPIO.output(19,GPIO.HIGH)

def LightGrn():
    LightsOff()
    GPIO.output(6,GPIO.HIGH)

Main()

GPIO.cleanup()
