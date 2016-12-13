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

	nums=[]
	if body:									#If the text is found on the page, do stuff.
		print name
		for child in body:
			number = child.string
			if len(number) <= 2:
				nums.append(number)
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
	return Winnings
	
def CheckTicket(ls1, ls2):
	NoMatches = 1
	NumWhite = 0
	NumRed = 0
	ls1 = map(int, ls1)				#Force all values to integer (removing HTML formatting)
	ls2 = map(int, ls2)	
	print "My ticket : " + str(ls2)
	print "Win ticket: " + str(ls1)
	
	if (set(ls1).intersection(ls2)):
		NumMatch = len(set(ls1).intersection(ls2))
		if NumMatch == 6:
			print "JACKPOT!!"
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
		
	return CalcValue(NumWhite, NumRed)
	
def Check():
	url = ('http://www.powerball.com/')
	name = "Powerball".ljust(15)
	winning_nums = CheckStock(url,name)
	MyWinnings = 0
	MyTickCount = 0
	
	while True:
		mytick = raw_input('Enter ticket numbers separated by spaces or "q" to quit: ')
		if mytick is 'q' or mytick == '':
			break		
		MyTicket = mytick.split()
		
		print "\n\nChecking ticket: "
		TickWinnings = CheckTicket(ls1 = winning_nums, ls2 = MyTicket)	
		MyTickCount += 1;
		MyWinnings += TickWinnings 
	print "In %d tickets, winnings are: $%d" %(MyTickCount, MyWinnings)

Check()	