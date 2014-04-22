#!/usr/bin/env python

from time import sleep
import yql

class Geocode(object):
	def __init__(self):
		self.results = None
	
	def connect(self):
		api_key = 'dj0yJmk9NWM0azdWc0xWMTZJJmQ9WVdrOU5qTkJUbTlxTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wMQ--'
		api_secret = '737f0bc32079f654abf72d125d103dc6f900fa79'
		
		conn = yql.Public(api_key = api_key, shared_secret = api_secret)
		
		return conn
		
	def query(self, location):
		conn = self.connect()
		
		q = 'SELECT * FROM geo.placefinder WHERE text = @text'
		statement = conn.execute(q, {"text": "Silver Spring, MD"})
		result =  statement.results['Result']['city']
		
		sleep(1)
		
		return result
