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
     	
def extract_tweeters():
	"""
	Extract all users with geographic information.
	"""
	
	users = {}
	
	conn = get_database_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT user_name, twitter_user_id, location_string FROM tweeter_tweeter LIMIT 10')
	
	for user_name, twitter_user_id, location_string in cursor.fetchall():
		if location_string is not None:
			user = users.get(twitter_user_id, Tweeter(twitter_user_id))
			user.location = location_string
			user.user_name = user_name

                        users[twitter_user_id] = user
        
        cursor.close()
        conn.close()

        return users.values()

if __name__ == '__main__':
	users = extract_tweeters()

	
        for user in users:
		u = Geocode(user.location)
		if u.identify_gps() == True:
			u.reverse_query()
		else:
			u.query()
