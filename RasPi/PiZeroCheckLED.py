import urllib2
from bs4 import BeautifulSoup
import re
import time, threading
import RPi.GPIO as GPIO

# Set GPIO pins
RedPin = 5
BluPin = 6
GrnPin = 13

# Set GPIO up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RedPin,GPIO.OUT)
GPIO.setup(BluPin,GPIO.OUT)
GPIO.setup(GrnPin,GPIO.OUT)

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Google Chrome')]

def CheckStock(url, name):
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl, "html.parser")
	title = soup.title.text
	body = soup.find(text="OUT OF STOCK")	   #Searches for text
	tag_pr = soup.find(id="prod-price").string
	price = ' '.join(tag_pr.split())
	tag_stk = soup.find(id="prod-stock").findNext(id="prod-stock").next_element #Find second item with id and set value to its next element.
	stock = ""
	if tag_stk:
		stock = ' ' .join(tag_stk.split())		#Get rid of tabs and newlines. Joins elements by space.
	else:
		stock = "Couldn't find that..."
	
	
	FuncReturn = 0
	if body:									#If the text is found on the page, do stuff.
		print name
		print "...............Price:",price
		print "...............Stock: Out of Stock\n"
	else:
		print name
		print "...............Price:",price
		print "...............Stock:",stock.capitalize()
		FuncReturn = 1
		
		return FuncReturn


def Check(interval):
	try:
		LightsOff()
		while True:
			ColorSet = [0,0,0]
			NumStock = 0
			url = ('https://www.adafruit.com/products/2885')
			name = "PiZero".ljust(15)
			if CheckStock(url,name):
				ColorSet=[1,0,0]
				NumStock += 1

			url = ('https://www.adafruit.com/product/2816')
			name = "PiZero Starter".ljust(15)
			if CheckStock(url,name):
				ColorSet=[0,1,0]
				NumStock += 1

			url = ('https://www.adafruit.com/product/2817')
			name = "PiZero Budget".ljust(15)
			if CheckStock(url,name):
				ColorSet=[0,0,1]
				NumStock += 1
				
			if NumStock == 3:
				ColorSet = [1,1,1]
			
			LightRGB(ColorSet)
			
			time.sleep(interval)
	except KeyboardInterrupt:
		GPIO.cleanup
	
def LightsOff():
	GPIO.output(RedPin,GPIO.LOW)
	GPIO.output(GrnPin,GPIO.LOW)
	GPIO.output(BluPin,GPIO.LOW)

def LightRGB(RGB):
	GPIO.output(RedPin,int(RGB[0])
	GPIO.output(GrnPin,int(RGB[1])
	GPIO.output(BluPin,int(RGB[2])

def PowerUp():
	LightRGB([1,0,0])
	time.sleep(1)
	LightRGB([0,1,0])
	time.sleep(1)
	LightRGB([0,0,1])
	time.sleep(1)
	
PowerUp()
Check(1800)	