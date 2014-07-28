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
                user = {}
                user['location'] = location_string
                user['user_name'] = user_name
                user['user_id'] = id
                
                users[id] = user
    elif table == 'users_2014':
        for user_id, location in cursor.fetchall():
            if location is not None:
                user = {}
                user['location'] = location
                user['user_id'] = user_id

                users[user_id] = user
        
    cursor.close()
    conn.close()

    return users.values()

if __name__ == '__main__':
    table = 'users_2014'
    
    users = extract_tweeters(table)

    for user in users:
        try:
            geolocation = Geocode(user['location'], user_id = user['user_id'])
            insert_record(geolocation.results, "user_locations_2014")
        except:
            traceback.print_exc(file=sys.stdout)
