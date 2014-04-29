#!/usr/bin/env python

"""Extract twitter data from mysql for use with sentiment analysis.

./extract.py > file
"""

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from tweeter import *
from geocode import *
from db import get_database_connection
from insert_dict import *
     	
def extract_tweeters():
	"""
	Extract all users with geographic information.
	"""
	
	users = {}
	
	conn = get_database_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT user_name, id, location_string FROM tweeter_tweeter')
	
	for user_name, id, location_string in cursor.fetchall():
		if location_string is not None:
			user = users.get(id, Tweeter(id))
			user.location = location_string
			user.user_name = user_name

                        users[id] = user
        
        cursor.close()
        conn.close()

        return users.values()

if __name__ == '__main__':
	users = extract_tweeters()

	
        for user in users:
		try:
			u = Geocode(user.location)
			if u.identify_gps() == True:
				u.reverse_query()
			else:
				u.query()
				u.results['user_name'] = user.user_name
				u.results['id'] = user.id
				u.results['stop_words_count'] = u.stop_words_count
			insert_record(u.results, "user_locations")
		except:
			print "Unexpected error:", sys.exc_info()[0]
