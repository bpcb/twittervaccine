#!/usr/bin/env python

"""Sum up statistics about twitter training data.

Yes, I realize there are just group bys...
"""

from extract import *
from collections import Counter

counter = Counter()

for tweet in extract():
    counter[tweet.get_majority_vote()] += 1

print counter

total = sum(counter.values())
fracs = [(key, float(val) / total) for (key, val) in counter.iteritems()]
print fracs

