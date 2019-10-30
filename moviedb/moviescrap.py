"""
	experiment how to retrieve a few (1 to 10) pictures to illustrate a movie
	identified from its title, its director
	the bigger images are preferred
	source of the images is either google or imdb

"""
from bs4 import BeautifulSoup
from googlesearch import search
from io import BytesIO
import logging
import logging.config
from PIL import Image
import re
import requests
import string
import urllib.request


DEBUG = False



logger = logging.getLogger(__name__)  # once in each module

class MovieScrap:
	MAXREP = 10
	MAXPICS = 5
	INTERVAL = 2 # in seconds
	def __init__(self):
		self.queryDict= {"Title":"", "Director":"", "Other":""}
		self.results=[]
		self.punctuation = string.punctuation +'\'-_'+"'"
		self.maxRelevance = 0
		self.maxSize = 0
	
	def __str__(self):
		return " ".join(self.queryWords)
	
	def collect_interactive_query(self):
		for k in self.queryDict.keys():
			self.queryDict[k]=input("_"+k+": ")
		self.setQueryStr(" ".join(self.queryDict.values()).strip())
	
	def setQueryStr(self, s):
		self.queryStr = s.strip()
		self.queryWords = self.clean(self.queryStr)
	
	def filename(url):
		#
		# exclude domain name and dir path
		# keep filename
		#
		fn=url[url.rfind("/")+1:].lower()
		# exclude .jpeg ending
		if fn.endswith(".jpg"):
			return fn[:-4]
		if fn.endswith(".jpeg"):
			return fn[:-5]
		return fn
	
	def domain(url):
		return url.split("//")[-1].split("/")[0]
		
	
	def clean(self,s):
		for c in self.punctuation:
			s=s.replace(c,' ')
		return s.lower().strip().split(' ')
	
	def relevance(self,link,alt):
		#
		# relevance is the count of matches of query terms...
		#
		r=0
		#
		# ...and of filename
		#
		fn=self.clean(MovieScrap.filename(link))
		for w in self.queryWords:
				if w in fn:
					r=r+1
		#
		# ...plus, if available, of alt text
		#
		if alt:
			at = self.clean(alt)
			for w in self.queryWords:
				if w in at:
					r=r+1 
		#
		return r
	
	
	def insertResult(self,link, relevance, size):
		#
		# check if link is known
		#
		if link in map(lambda t: t[2],self.results):
			return
		#
		# check if result is an improvement
		#
		if (relevance,size)< (self.maxRelevance, self.maxSize):
			return
		#
		# append new result
		#
		self.maxRelevance, self.maxSize = relevance, size
		self.results.append((relevance, size, link))

		

	def scrapPics(self):
		#
		# add some keywords like movie, images to the query
		#
		q1 = self.queryStr + " poster film "
		#
		# target relevance is the number of words in the query
		# each could be found once in the filename
		# and once in the alt text
		#
		targetRelevance = q1.count(" ")+1
		#
		#
		#
		for url in search(q1, stop=MovieScrap.MAXREP, pause=MovieScrap.INTERVAL):
			#
			# explore url for images
			#
			logger.debug("... exploring "+url)
			try:
				response= requests.get(url)
			except requests.exceptions.SSLError:
				logger.info("Max retries exceeded - Certificate verif failed")
				continue
			except Exception as e:
				logger.error("Unexpected exception when accessing pic "+str(e))
				continue
			soup = BeautifulSoup(response.text, "html.parser")
			for raw_img in soup.find_all('img',{'src':re.compile(r'\.jpe?g')}):
				link = raw_img.get('src')
				alt = raw_img.get('alt',"")
				if link is not None:
					#
					# check availability and size
					#
					try:
						image_raw = requests.get(link)
						image = Image.open(BytesIO(image_raw.content))
						width, height = image.size
						self.insertResult(link, self.relevance(link, alt), width*height)
						if len(self.results)>MovieScrap.MAXPICS:
							self.results = self.results[-MovieScrap.MAXPICS:]
					except requests.exceptions.MissingSchema:
						logger.info("Unreachable pic")
						continue
					except Exception as e:
						logger.error("Unexpected exception when retrieving pic details "+str(e))
						continue
			#
			# exploring more sites ceases as soon as 
			# target relevance is reached
			#
			if self.maxRelevance >= targetRelevance:
				return

	def scrapImdb(self):
		#
		# When  movie title and director name are ok, the first answer 
		# from imdb is ok (unless it's an add - TODO check)
		#
		q1 = "imdb "+ self.queryStr
		#
		# In the unlikely case where nothing is found, None is a convenient
		# return value
		#
		for url in search(q1, stop=MovieScrap.MAXREP, pause=MovieScrap.INTERVAL):
			return url


def main():
	logging.config.dictConfig({
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'console': {
				'format': '%(name)-12s %(levelname)-8s %(message)s'
			},
		},
		'handlers': {
			'console': {
				'class': 'logging.StreamHandler',
				'formatter': 'console'
			},
		},
		'loggers': {
			'': {
				'level': 'INFO',
				'handlers': ['console', ]
			}
		}
	})
	while True:
		mps= MovieScrap()
		mps.collect_interactive_query()
		print(mps)
		if mps.queryStr=="":
			break
		mps.scrapPics()
		for i in mps.results:
			print(i)
		print(mps.scrapImdb())

if __name__=='__main__':
	main()

