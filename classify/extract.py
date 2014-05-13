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

def extract_classified_tweets(collapse_labels=True):
    """Extract all tweets with at least one sentiment vote.

    Tweets with ties in the majority vote count are omitted.
    Return a list of Tweet objects.
    """

    tweets = {}

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT tweet_id, vote FROM majority_vote_unique')

    for _id, vote in cursor.fetchall():
        tweet = tweets.get(_id, Tweet(_id))
        tweet.majority_vote = vote
        if collapse_labels and vote != '-':
            tweet.majority_vote = 'X'
        tweets[_id] = tweet

    sql = 'SELECT T.id, T.text FROM tweets_tweet AS T '
    sql += 'WHERE EXISTS (SELECT * FROM majority_vote_unique AS V WHERE T.id=V.tweet_id)'
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
    for tweet in extract_classified_tweets():
        print tweet
