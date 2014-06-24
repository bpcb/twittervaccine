#!/usr/bin/env python

"""Extract twitter data from mysql for use with sentiment analysis.

./extract.py > file
"""

import sys
import traceback

# Hack: append common/ to sys.path
sys.path.append("../common")

from tweeter import *
from geocode import *
from db import get_database_connection
from insert_dict import *

def extract_tweeters(table):
	"""
	Extract all users with geographic information.
	"""
	
	if table != 'users_2014' and table != 'tweeter_tweeter':
		print 'extract_tweeters function only works with tables of users (users_2014 and tweeter_tweeter)'
		break
	
	users = {}
	
	conn = get_database_connection(port = 2001)
	cursor = conn.cursor()
	
	# This execute statement depends on which table you are trying to extract users from.
	# If 2009 dataset, use 'SELECT user_name, id, location_string FROM tweeter_tweeter'
	if table == 'users_2014':
		cursor.execute('SELECT user_id, location FROM users_2014')
	elif table == 'tweeter_tweeter':
		cursor.execute('SELECT user_name, id, location_string FROM tweeter_tweeter')
	
	if table == 'tweeter_tweeter':
		for user_name, id, location_string in cursor.fetchall():
			if location_string is not None:
				user = users.get(id, Tweeter(id))
				user.location = location_string
				user.user_name = user_name
				users[id] = user
	elif table == 'users_2014':
		for user_id, location in cursor.fetchall():
			if location is not None:
				user = users.get(user_id, Tweeter(user_id))
				user.location = location
		
	cursor.close()
	conn.close()

	return users.values()

if __name__ == '__main__':
	table = 'users_2014'
	
	users = extract_tweeters(table)

	for user in users:
		try:
			u = Geocode(user.location)
			if u.identify_gps() == True:
				u.reverse_query()
			else:
				u.query()

				u.results['user_name'] = user.user_name
				u.results['id'] = user.user_id
				u.results['stop_words_count'] = u.stop_words_count

				insert_record(u.results, "user_locations")
		except:
			traceback.print_exc(file=sys.stdout)
