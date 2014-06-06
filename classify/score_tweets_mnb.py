#!/usr/bin/env python

"""Compute naive bayes sentiment scores; store in the database."""

import extract
import publish
from scikit_nb_scorer import MultinomialNBScorer

scorer = MultinomialNBScorer()
results = [(_id, scorer.get_document_score(text, normalize=False))
           for (_id, text) in extract.extract_text()]
publish.publish_sentiment('naivebayes', results)

print 'published %d results' % len(results)
