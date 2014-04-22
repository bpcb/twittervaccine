#!/usr/bin/env python

from time import sleep
import yql

reverse_identifiers = ['\xc3\x9cT:', 'iPhone:']

class Geocode(object):
	def __init__(self, location):
		self.results = None
		self.location = location
	
	def connect(self):
		api_key = 'dj0yJmk9NWM0azdWc0xWMTZJJmQ9WVdrOU5qTkJUbTlxTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wMQ--'
		api_secret = '737f0bc32079f654abf72d125d103dc6f900fa79'
		
		conn = yql.Public(api_key = api_key, shared_secret = api_secret)
		
		return conn
		
	def query(self):
		conn = self.connect()
		
		q = 'SELECT * FROM geo.placefinder WHERE text = @text'
		statement = conn.execute(q, {"text": self.location})
		print "String location:", self.location
		
		result = None
		if statement.results is not None:
			result = statement.results['Result']
			print result
		sleep(1)
		
		return result

	def reverse_query(self):
		"""
		Query Yahoo YQL for locations that have identifiers that
		indicate the location is a pair of lat, long coordinates.
		"""
		conn = self.connect()
		location_stripped = self.strip_reverse_identifiers()		

		q = 'SELECT * FROM geo.placefinder WHERE text = @text '
		q += 'AND gflags = \"R\"'
		print q
		statement = conn.execute(q, {"text": location_stripped})
		print "String location:", location_stripped
	
		result = None
		if statement.results is not None:
			for i in statement.results['Result']:
				print statement.results['Result'][i]
		sleep(1)
		
		return result	

	def identify_gps(self):
		"""
		Identifies whether a location string contains words that
		identify it as a pair of GPS coordinates.
		"""
		
		loc_words = self.location.split()
		for word in loc_words:
			for id in reverse_identifiers:
				if word == id:
					return True
		
		return False

	def remove_stop_words(self):
		pass

	def strip_reverse_identifiers(self):
		loc_words = self.location.split()
		no_rev_ids = [word for word in loc_words if word not in reverse_identifiers]
		
		return " ".join(no_rev_ids)


	
