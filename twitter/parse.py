#!/usr/bin/env python

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

import json, glob
from insert_dict import insert_record

"""
Parse tweets as emitted by the twitter API.
"""


for json_file in glob.glob('/mnt/tweets*.json'):
    print json_file
    with open(json_file) as f:
        for line in f:
            obj = json.loads(line)
            print obj

            tweet = dict()
            user = dict()        
        
            tweet['tweet_id'] = obj['id']
            tweet['user_id'] = obj['user']['id']
            tweet['text'] = obj['text']
            tweet['created_at'] = obj['created_at']

            user['user_id'] = obj['user']['id']
            user['user_name'] = obj['user']['screen_name']
            user['location'] = obj['user']['location']
        
            insert_record(tweet, 'tweets_2014')
            insert_record(user, 'users_2014')
