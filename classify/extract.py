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

def extract_text(table, limit=0):
    """Extract (tweet_id, text) from the database for all tweets from given table of tweets.

    If limit is non-zero, return this many tuples.
    """
    conn = get_database_connection()
    cursor = conn.cursor()

	# SQL statement should read SELECT id, text FROM %s' % (table) if using old tweets
    sql = 'SELECT tweet_id, text FROM %s' % (table)
    cursor.execute(sql)

    if limit > 0:
        return cursor.fetchmany(limit)
    else:
        return cursor.fetchall()

def extract_classified_tweets(collapse_labels=True, limit=0):
    """Extract all tweets with at least one sentiment vote.

    Tweets with ties in the majority vote count are omitted.

    Return an iterator of tuples of the form (id, vote, text)
    """

    conn = get_database_connection()
    cursor = conn.cursor()
    query = 'SELECT V.tweet_id, V.vote, T.text FROM majority_vote_unique AS V'
    query += ' JOIN tweets_tweet AS T ON V.tweet_id=T.id'

    if limit > 0:
        query += ' LIMIT %d' % limit

    cursor.execute(query)

    try:
        for _id, vote, text in cursor.fetchall():
            if collapse_labels and vote != '-':
                vote = 'X'
            yield (_id, vote, text)
    finally:
        cursor.close()
        conn.close()

def extract_labeled_tweets(limit=0):
    """Extract all tweets with a revised label.

    Return an iterator of tuples of the form (id, vote, text)
    """

    conn = get_database_connection()
    cursor = conn.cursor()
    query = 'SELECT L.id, L.label, T.text FROM revised_labels AS L'
    query += ' JOIN tweets_tweet AS T ON L.id=T.id'

    if limit > 0:
        query += ' LIMIT %d' % limit

    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

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
