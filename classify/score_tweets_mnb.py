#!/usr/bin/env python

"""Compute naive bayes sentiment scores; store in the database."""

import extract
import publish
from scikit_scorer import *
import numpy as np

scorer = ScikitScorer(create_naive_bayes_classifier())
results = []
for i, (_id, text) in enumerate(extract.extract_text()):
    score = np.asscalar(scorer.get_document_score(text))
    results.append((_id, score))
    if (i % 1000) == 0:
        print "%d" % i

publish.publish_sentiment('naivebayes', results)

print 'published %d results' % len(results)
