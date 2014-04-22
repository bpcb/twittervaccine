#!/usr/bin/env python

"""Publish sentiment data to the database."""

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS user_locations(
	twitter_user_id BIGINT,
	user_name VARCHAR(64), 
	quality SMALLINT,
	latitude FLOAT,
	longitude FLOAT,
	offsetlat FLOAT,
	offsetlon FLOAT,
	radius SMALLINT,
	name VARCHAR(64),
	line1 VARCHAR(64),
	line2 VARCHAR(64),
	line3 VARCHAR(64),
	line4 VARCHAR(64),
	house VARCHAR(64),
	street VARCHAR(64),
	xstreet VARCHAR(64),
	unittype VARCHAR(64),
	unit VARCHAR(64),
	postal VARCHAR(64),
	neighborhood VARCHAR(64),
	city VARCHAR(64),
	county VARCHAR(64),
	countrycode VARCHAR(64),
	statecode VARCHAR(64),
	countrycode VARCHAR(64),
	uzip VARCHAR(64),
	hash VARCHAR(64),
	woeid VARCHAR(64),
	woetype VARCHAR(64),	
	PRIMARY KEY (twitter_user_id));
"""

INSERT_SQL = """
INSERT INTO user_locations(
	(twitter_user_id,
	user_name,
	quality,
	latitude,
	longitude,
	offsetlat,
	offsetlon,
	radius,
	name,
	line1,
	line2,
	line3,
	line4,
	house,
	street,
	xstreet,
	unittype,
	unit,
	postal,
	neighborhood,
	city,
	county,
	countrycode,
	statecode,
	countrycode,	
	uzip,
	hash,
	woeid,
	woetype)
	VALUES (%s, %s, %s, %s);
"""

def publish_sentiment(algorithm, tweets):
    """Store a list of sentiment analysis results into the data base.

    :param algorithm: The algorithm used to classify tweets; can be a string or
    or an integer.
    :param tweets: An iterable list of (tweet_id, sentiment_score) tuples.
    """

    rev = git_rev.git_current_revision()
    if isinstance(algorithm, str):
        algo = ALGORITHMS[algorithm]
    else:
        algo = algorithm

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_SQL)

    for _id, score in tweets:
        cursor.execute(INSERT_SQL, [_id, algo, rev, score])

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # create some dummy test data
    tweets = [(1, -.9), (2, -.3), (3, .7), (4, 0.0), (5, 1.1)]
    publish_sentiment('test', tweets)

