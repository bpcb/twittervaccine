#!/usr/bin/env python

"""Compute VSPS sentiment scores; store in the database."""

import extract
import score
import publish

scorer = score.SentimentScorer.from_vaccine_phrases()
results = [(_id, scorer.get_document_score(text, normalize=False))
           for (_id, text) in extract.extract_text()]
publish.publish_sentiment('vsps', results)

print 'published %d results' % len(results)

