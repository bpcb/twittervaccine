#!/usr/bin/env python

"""Extract twitter data from mysql for use with sentiment analysis.

./extract.py > file
"""

import pickle
import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from tweet import *
from tweeter import *
from geocode import *

from db import get_database_connection

def extract_text(limit=0):
    """Extract (tweet_id, text) from the database for all tweets.

    If limit is non-zero, return this many tuples.
    """
    conn = get_database_connection()
    cursor = conn.cursor()

    sql = 'SELECT id, text FROM tweets_tweet'
    cursor.execute(sql)

    if limit > 0:
        return cursor.fetchmany(limit)
    else:
        return cursor.fetchall()

def extract():
    """Extract all tweets with at least one sentiment vote.

    Return a list of Tweet objects.
    """

    tweets = {}

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT tweet_id, vote, count FROM vote_count')

    for _id, vote, count in cursor.fetchall():
        tweet = tweets.get(_id, Tweet(_id))
        tweet.add_votes(vote, count)
        tweets[_id] = tweet

    sql = 'SELECT T.id, T.text FROM tweets_tweet AS T '
    sql += 'WHERE EXISTS (SELECT * FROM vote_count AS V WHERE T.id=V.tweet_id)'
    cursor.execute(sql)

    for _id, text in cursor.fetchall():
        tweet = tweets[_id]
        tweet.text = text

    cursor.close()
    conn.close()

    return tweets.values()
	
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
    # dump results to standard out
	users = extract_tweeters()

        for user in users:
            print Geocode.query(user.location)
	
    # for tweet in extract():

        # pickle.dump(tweet, sys.stdout)
