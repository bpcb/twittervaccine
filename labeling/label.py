#!/usr/bin/env python

"""Script for labeling randomly selected tweets.

Results stored in LABELS.txt
"""

import os
import random
import sys

sys.path.append("../common")
from db import get_database_connection

OUTPUT_FILE = 'LABELS.txt'

if os.path.exists(OUTPUT_FILE):
    print 'ERROR: output file %s already exists' % OUTPUT_FILE
    sys.exit(1)

conn = get_database_connection(2001)
cursor = conn.cursor()

# Select tweets from among those classified by the PSU study
query = 'SELECT V.tweet_id, T.text FROM majority_vote_unique AS V'
query += ' JOIN tweets_tweet AS T ON V.tweet_id=T.id'

cursor.execute(query)
result = list(cursor.fetchall())
random.shuffle(result)

# z = Positive
# x = Neutral
# c = Negative
labels = []
try:
    for _id, text in result:
        while True:
            ch = raw_input("%d %s : " % (_id, text))
            if ch in ['z', 'x', 'c']:
                labels.append((_id, ch))
                break
            else:
                print 'Choose either z (positive), x (neutral), or c (negative)'
finally:
    with open(OUTPUT_FILE, 'w') as fh:
        for _id, label in labels:
            fh.write('%d, %s\n' % (_id, label))
