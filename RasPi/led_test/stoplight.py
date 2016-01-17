import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def Main():
    try:
        while True:
            LightsOff()
            InputState = GPIO.input(22)
            if InputState == False:
                print('Button pressed')
                RGB()
                time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup

def Light():
    GPIO.output(6,GPIO.HIGH)
    GPIO.output(17,GPIO.HIGH)
    GPIO.output(19,GPIO.HIGH)

def RGB():
    SleepTime = 0.5
    LightsOff()
    time.sleep(SleepTime)
    LightRed()
    time.sleep(SleepTime)
    LightBlu()
    time.sleep(SleepTime)
    LightGrn()
    time.sleep(SleepTime)
    LightWht()
    time.sleep(SleepTime)
    LightsOff()

def LightsOff():
    GPIO.output(21,GPIO.LOW)
    GPIO.output(12,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(6,GPIO.LOW)
    GPIO.output(17,GPIO.LOW)
    GPIO.output(19,GPIO.LOW)

def LightWht():
    LightsOff()
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(21,GPIO.HIGH)

def LightRed():
    LightsOff()
    GPIO.output(12,GPIO.HIGH)

def LightBlu():
    LightsOff()
    GPIO.output(21,GPIO.HIGH)

def LightGrn():
    LightsOff()
    GPIO.output(16,GPIO.HIGH)

Main()

GPIO.cleanup()
