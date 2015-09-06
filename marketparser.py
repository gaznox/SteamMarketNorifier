import time
import urllib
import urllib2
from urllib2 import urlopen
import re
import cookielib, urllib2
from cookielib import CookieJar
import datetime

titlear = []
pricear = []
stickerar = []

#Add URL's to be parsed
urlar = [
'http://steamcommunity.com/market/listings/730/USP-S%20%7C%20Guardian%20%28Factory%20New%29?filter=%22%28holo%29+%7C+Katowice+2014%22', 
'http://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Blood%20Tiger%20%28Factory%20New%29?filter=%22%28holo%29+%7C+Katowice+2014%22',
'http://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Blood%20Tiger%20%28Factory%20New%29?filter=howling',
'http://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Cobalt%20Disruption%20%28Factory%20New%29?filter=%22%28holo%29+%7C+Katowice+2014%22',
'http://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Cobalt%20Disruption%20%28Factory%20New%29?filter=%22Titan+%28Holo%29+%7C+Katowice+2014%22',
'http://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Candy%20Apple%20%28Factory%20New%29?filter=%22holo+%7C+katowice+2014%22',
'http://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Candy%20Apple%20%28Factory%20New%29?filter=howling',
'http://steamcommunity.com/market/listings/570/Genuine%20Bow%20of%20the%20Master%20Thief'
]

reqar = [
200,
200,
250,
400,
500,
300,
300,
20
]

#Add Pushingbox Key
key = ""

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


def main():
	index=-1
	for link in urlar:
		index+=1
		#print reqar[index]
		searchURL(link, index)



def searchURL(url, pos):
	try:
		titlear = []
		pricear = []
		stickerar = []
		sourceCode = opener.open(url).read()

		#print sourceCode

		try:
			titles = re.findall(r'{"listingid":"(.*?)",',sourceCode)
			prices = re.findall(r',"price":(.*?),"',sourceCode)
			stickers = re.findall(r'<br>Sticker: (.*?)<',sourceCode)
			for title in titles:
				#print title
				titlear.append(title)
			for price in prices:
				#print price
				pricear.append(price)
			for sticker in stickers:
				#print sticker
				stickerar.append(sticker)
		except Exception, e:
			print "Find error: "+str(e)

		#print titlear
		#print pricear
		#print stickerar


		priceCheck(titlear, pricear, stickerar, pos)


		#for index, item in enumerate(stickerar):
		#	if item == "Titan (Holo) | Katowice 2014" and int(pricear[index]) <= 500:
		#		pushingbox(item, stickerar[0])
		#		print index, item, pricear[index]

	except Exception,e:
		print "Open error: "+str(e)
		pass


def priceCheck(title, price, sticker, itemIndex):
	#print itemIndex
	#print reqar[itemIndex]

	try:
		if int(price[0]) <= reqar[itemIndex]:
			print "Recommended buy: ", price[0], sticker[0]
			pushingbox(price[0], sticker[0], urlar[itemIndex])
	except Exception,e:
		print "Price chek error: "+str(e)
		pass


def pushingbox(price, sticker, url):
	a = urllib.urlopen('http://api.pushingbox.com/pushingbox?devid='+key+'&price='+price+'&sticker='+sticker+'&url='+url)
	a.close()

main()
