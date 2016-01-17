import RPi.GPIO as GPIO
import time
import random

RedPin = 5
BluPin = 6
GrnPin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RedPin,GPIO.OUT)
GPIO.setup(BluPin,GPIO.OUT)
GPIO.setup(GrnPin,GPIO.OUT)

def Main():
    try:
        LightsOff()
        while True:
            request = raw_input("Enter RGB (0=off, 1=on) -->")
            if (len(request) == 3):
                GPIO.output(RedPin,int(request[0]))
                GPIO.output(GrnPin,int(request[1]))
                GPIO.output(BluPin,int(request[2]))
            if (request == 'exit'):
                GPIO.cleanup
                break
            if ('rand' in request):
                interval = float(raw_input("Enter time in seconds to switch colours..."))
                while True:
                    value = [int(random.getrandbits(1)), int(random.getrandbits(1)), int(random.getrandbits(1))]     
                    print "Values are: ", value[0:3]
                    GPIO.output(RedPin,int(bool(random.getrandbits(1))))
                    GPIO.output(GrnPin,int(bool(random.getrandbits(1))))
                    GPIO.output(BluPin,int(bool(random.getrandbits(1))))
                    time.sleep(interval)
    except KeyboardInterrupt:
        GPIO.cleanup


def LightsOff():
    GPIO.output(RedPin,GPIO.LOW)
    GPIO.output(GrnPin,GPIO.LOW)
    GPIO.output(BluPin,GPIO.LOW)


Main()
