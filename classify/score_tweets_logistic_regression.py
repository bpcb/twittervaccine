#!/usr/bin/env python

# Andrew Whitaker

"""Compute sentiment scores using logistic regression; store in the database."""

import extract
import publish
from scikit_scorer import *
import numpy as np

scorer = ScikitScorer(create_logistic_regression_classifier())
results = []
for i, (tweet_id, text) in enumerate(extract.extract_text('tweets_2014')):
    score = np.asscalar(scorer.get_document_score(text))
    results.append((tweet_id, score))
    if (i % 1000) == 0:
        print "%d" % i

publish.publish_sentiment('logistic', results)

print 'published %d results' % len(results)
