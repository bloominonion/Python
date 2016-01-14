import urllib2
from bs4 import BeautifulSoup
import re
import time, threading

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Google Chrome')]

def CheckStock(url, name):
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl, "html.parser")
	title = soup.title.text
	body = soup.find_all('span')	   #Searches for text
	#tag_stk = soup.find(id="prod-stock").findNext(id="prod-stock").next_element #Find second item with id and set value to its next element.

	nums=[]
	if body:									#If the text is found on the page, do stuff.
		print name
		#print body.findNext('class="balls"')
		for child in body:
			number = child.string
			if len(number) <= 2:
				nums.append(number)
		#print body.span.next
		#print body.span.findNext("span").next
	else:
		print "Not found..."
		
	#RedBall=nums.pop()	
	#for num in nums:
	#	print "White ball:", num
	#	
	#print "Red ball  :", RedBall
	return nums

def CalcValue(nWhite,nRed):
	Winnings = 0
	if (nWhite == 0 and nRed == 1):
		Winnings = 4
	if (nWhite == 1 and nRed == 1):
		Winnings = 4
	if (nWhite == 2 and nRed == 1):
		Winnings = 7
	if (nWhite == 3 and nRed == 0):	
		Winnings = 7
	if (nWhite == 3 and nRed == 1):
		Winnings = 100
	if (nWhite == 4 and nRed == 0):	
		Winnings = 100
	if (nWhite == 4 and nRed == 1):
		Winnings = 50000
	if (nWhite == 5 and nRed == 0):
		Winnings = 1000000
	if (nWhite == 5 and nRed == 1):
		Winnings = "Jackpot"

	print "Winnings is $" + str(Winnings)
	
def CheckTicket(ls1, ls2):
	NoMatches = 1
	NumWhite = 0
	NumRed = 0
	ls1 = map(int, ls1)				#Force all values to integer (removing HTML formatting)
	print "My ticket : " + str(ls2)
	print "Win ticket: " + str(ls1)
	
	if (set(ls1).intersection(ls2)):
		NumMatch = len(set(ls1).intersection(ls2))
		if NumMatch == 6:
			print "JACKPOT!!"
		#else:
		#	print "Ordered matches!", set(ls1).intersection(ls2)
		NoMatches = 0
	
	WinRed = ls1.pop()
	MyRed  = ls2.pop()
	
	if (set(ls1) & set(ls2)):
		print "Found unordered matches:", set(ls1) & set(ls2)
		NumWhite = len(set(ls1) & set(ls2))
		NoMatches = 0
	
	if (WinRed == MyRed):
		print "Matched powerball!"
		NumRed = 1
		NoMatches = 0
	
	if NoMatches:
		print "No matches found"
		
	CalcValue(NumWhite, NumRed)
	
def Check(interval):
	url = ('http://www.powerball.com/')
	name = "Powerball".ljust(15)
	winning_nums = CheckStock(url,name)
	MyTicket1 = [1,5,16,17,20,20]
	MyTicket2 = [8,16,30,50,60,10]
	MyTicket3 = [2,9,20,35,38,16]
	MyTicket4 = [5,30,38,61,69,16]
	MyTicket5 = [3,4,6,34,65,21]
	
	print "\n\nChecking ticket: 1"
	CheckTicket(ls1 = winning_nums, ls2 = MyTicket1)	
	print "\n\nChecking ticket: 2"
	CheckTicket(ls1 = winning_nums, ls2 = MyTicket2)	
	print "\n\nChecking ticket: 3"
	CheckTicket(ls1 = winning_nums, ls2 = MyTicket3)	
	print "\n\nChecking ticket: 4"
	CheckTicket(ls1 = winning_nums, ls2 = MyTicket4)	
	print "\n\nChecking ticket: 5"
	CheckTicket(ls1 = winning_nums, ls2 = MyTicket5)

	
	#threading.Timer(interval,Check).start()

Check(120)	