#!/usr/bin/env python

# Andrew Whitaker

"""Compute sentiment scores using logistic regression; store in the database."""

import extract
import publish
from scikit_scorer import *
import numpy as np

scorer = ScikitScorer(create_logistic_regression_classifier())
results = []
for i, (_id, text) in enumerate(extract.extract_text()):
    score = np.asscalar(scorer.get_document_score(text))
    results.append((_id, score))
    if (i % 1000) == 0:
        print "%d" % i

publish.publish_sentiment('logistic', results)

print 'published %d results' % len(results)
