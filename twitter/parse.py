#!/usr/bin/env python

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

import json, glob
from insert_dict import insert_record

"""
Parse tweets as emitted by the twitter API.
"""

user_errors = open('user_errors.txt', 'w')
tweet_errors = open('tweet_errors.txt', 'w')


for json_file in glob.glob('/mnt/tweets*.json'):
	print json_file
	with open(json_file) as f:
		for line in f:
			try:
				obj = json.loads(line)
			except ValueError:
				continue

			tweet = dict()
			user = dict()		
		
			tweet['tweet_id'] = obj['id']
			tweet['user_id'] = obj['user']['id']
			tweet['text'] = obj['text']
			tweet['created_at'] = obj['created_at']

			user['user_id'] = obj['user']['id']
			user['user_name'] = obj['user']['screen_name']
			user['location'] = obj['user']['location']
		
			try:
				insert_record(tweet, 'tweets_2014')
			except UnicodeEncodeError:
				tweet_errors.write(str(tweet['tweet_id']) + '\n')
			try:
				insert_record(user, 'users_2014')
			except UnicodeEncodeError:
				user_errors.write(str(user['user_id']) + '\n')

user_errors.close()
tweet_errors.close()
