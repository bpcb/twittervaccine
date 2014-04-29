#!/usr/bin/env python

"""Compute afinn111 sentiment scores; store in the database."""

import extract
import score
import publish

scorer = score.SentimentScorer.from_afinn_111()
results = [(_id, scorer.get_document_score(text, normalize=False))
           for (_id, text) in extract.extract_text()]
publish.publish_sentiment('afinn111', results)

print 'published %d results' % len(results)

