import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

count = 0
blinks = 5
sleep = 0.5
while (count<blinks):
    time.sleep(sleep)
    GPIO.output(17,GPIO.HIGH)
    time.sleep(sleep)
    GPIO.output(17,GPIO.LOW)
    count = count + 1

GPIO.cleanup()
