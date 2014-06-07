#!/usr/bin/env python

"""Compute naive bayes sentiment scores; store in the database."""

import extract
import publish
from scikit_nb_scorer import MultinomialNBScorer

scorer = MultinomialNBScorer()
results = []
for i, (_id, text) in enumerate(extract.extract_text()):
    reults.append((_id, scorer.get_document_score(text)))
    if (i % 1000) == 0:
        print "%d" % i

publish.publish_sentiment('naivebayes', results)

print 'published %d results' % len(results)
