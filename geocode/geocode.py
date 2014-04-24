#!/usr/bin/env python

from time import sleep
import yql

#These are identifiers that sometimes preprend lat, long strings
REVERSE_IDENTIFIERS = ['\xc3\x9cT:', 'iPhone:']

#These stop words taken from Lucene's StopAnalyzer.java class. 
#Extra word: 'here' added, because strangely enough this resolves to somewhere in 
#India.
LUCENE_STOP_WORDS = [
	'a', 'and', 'are', 'as', 'at', 
	'be', 'but', 'by', 'for', 'if', 
	'in', 'into', 'is', 'it', 'no', 'not', 
	'of', 'on', 'or', 'such', 'that', 'the',
	'their', 'then', 'there', 'these', 'they', 
	'this', 'to', 'was', 'will', 'with', 'here',
]

class Geocode(object):
	def __init__(self, location):
		self.results = {}
		self.location = location
		self.stop_words_count = len([word for word in self.location.split() if word in LUCENE_STOP_WORDS])	
	
	def connect(self):
		api_key = 'dj0yJmk9NWM0azdWc0xWMTZJJmQ9WVdrOU5qTkJUbTlxTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wMQ--'
		api_secret = '737f0bc32079f654abf72d125d103dc6f900fa79'
		
		conn = yql.Public(api_key = api_key, shared_secret = api_secret)
		
		return conn
		
	def query(self):
		conn = self.connect()
		location_stripped = self.strip()

		q = 'SELECT * FROM geo.placefinder WHERE text = @text'
		statement = conn.execute(q, {"text": self.location})
		
		print location_stripped
		result = None
		if statement.results is None:
			print "no results!"
		elif isinstance(statement.results['Result'], (dict)):
			print "one result!"
			for i in statement.results['Result']:
				self.results[i] = statement.results['Result'][i]	
		else:
			print "multiple results!"
			for i in statement.results['Result'][0]:
				self.results[i] = statement.results['Result'][0][i]
		sleep(1)

	def reverse_query(self):
		"""
		Query Yahoo YQL for locations that have identifiers that
		indicate the location is a pair of lat, long coordinates.
		"""
		conn = self.connect()
		location_stripped = self.strip()	

		q = 'SELECT * FROM geo.placefinder WHERE text = @text '
		q += 'AND gflags = \"R\"'
		statement = conn.execute(q, {"text": location_stripped})
		
		print location_stripped
		result = None
		if statement.results is None:
			print "no results!"
		elif isinstance(statement.results['Result'], (dict)):
			print "one result!"
			for i in statement.results['Result']:
				self.results[i] = statement.results['Result'][i]
		else:
			print "multiple results!"
			for i in statement.results['Result'][0]:
				self.results[i] = statement.results['Result'][0][i]
		sleep(1)
			

	def identify_gps(self):
		"""
		Identifies whether a location string contains words that
		identify it as a pair of GPS coordinates.
		"""
		
		loc_words = self.location.split()
		for word in loc_words:
			for id in REVERSE_IDENTIFIERS:
				if word == id:
					return True
		
		return False
	
	def strip(self):
		loc_words = self.location.split()

		no_rev_ids = [word for word in loc_words if word not in REVERSE_IDENTIFIERS]
		no_stop_words = [word for word in no_rev_ids if word not in LUCENE_STOP_WORDS] 
		
		return " ".join(no_stop_words)


	

