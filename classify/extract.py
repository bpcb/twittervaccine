#!/usr/bin/env python

"""Extract twitter data from mysql for use with sentiment analysis.

./extract.py > file
"""

import MySQLdb
import pickle
import sys

from tweet import *

def get_database_connection():
    conn = MySQLdb.connect(host='localhost', user='root', db='vaccine')
    return conn
    
def extract():
    """Extract all tweets with at least one sentiment vote.

    Return an iterator of Tweet objects.
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

    return tweets.itervalues()

if __name__ == '__main__':
    # dump results to standard out
    for tweet in extract():
        pickle.dump(tweet, sys.stdout)

    
