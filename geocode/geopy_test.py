#!/usr/bin/env python

from geopy import geocoders, point
import csv
from time import sleep
import re
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

file_name = 'locations_test.csv'
out_file_name = 'locations_test_geocoded.csv'

def strip_reverse_identifiers(location):
	"Location strings can contain identifiers before lat/long strings. Strip those out."
	loc_words = location.split()
	no_rev_ids = [w for w in loc_words if w not in REVERSE_IDENTIFIERS]
	return " ".join(no_rev_ids)
	
def remove_stop_words(location):
	""" Remove stop words from the location string. We need to remove stop
	words and try because strings like 'Born in Texas' resolve to Texas,l
	Indiana (IN). Yes, there is a town in Indiana called Texas. """

	loc_words = location.split()
	no_stop_words = [w for w in loc_words if w.lower() not in LUCENE_STOP_WORDS]
	return " ".join(no_stop_words)
	
def reverse_geocode_location(location):
	""" Try to reserve geocode the location. Removes any extraneous known identifiers, 
	and reverse geocodes the remainder """
	no_stop_words = remove_stop_words(location)
	result = yahoo_reverse_geocode(strip_reverse_identifiers(no_stop_words))

	if result is not None:
		if result.ambiguous == False:
			return result
	return None
	
def main():
	# infile = csv.reader(open(file_name, 'r'), delimiter=',')
	# outfile = csv.writer(open(out_file_name, 'w'), delimiter=',')

	consumer_key = 'dj0yJmk9NWM0azdWc0xWMTZJJmQ9WVdrOU5qTkJUbTlxTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wMQ--'
	consumer_key_secret = '737f0bc32079f654abf72d125d103dc6f900fa79'
	
	geolocator = geocoders.YahooPlaceFinder(consumer_key = consumer_key, consumer_secret = consumer_key_secret)
	
	location = 'Washington DC'
	raw_output = geolocator.geocode(location)
	print raw_output
	
	# location = ''
	# address = None
	# latitude = None
	# longitude = None

	# for line in infile:
		# user = line[0]
		# location = line[1].replace('\n', '')
		
		# print location
		# raw_output = geolocator.geocode(location, raw = True)
		# print raw_output

		# print location
		
		# if location is not '':
			# gps = False
			# for id in REVERSE_IDENTIFIERS:
				# if re.search(id, location):
					# location = strip_reverse_identifiers(location)
					# coordinates = point.Point(latitude = float(location[-19:-10]), longitude = float(location[-10:]))
					# address = geolocator.reverse(coordinates) 
					# outfile.writerow([user, location, address, latitude, longitude])
					# gps = True
			# if gps == False:	
				# try:
					# location = remove_stop_words(location)
					# address, (latitude, longitude) = geolocator.geocode("%s" % (location))
					# outfile.writerow([user, location, address, latitude, longitude])
				# except:
					# outfile.writerow([user, location])
		# else:
			# outfile.writerow([user])
			
		# sleep(1)
		
		# y = yql.Public()
		# query = 'SELECT * FROM geo.placefinder WHERE text = @text AND api_key = @consumer_key';
		# y.execute(query, {"text": "Washington DC", "consumer_key": consumer_key})
		
if __name__ == '__main__':
	main()
