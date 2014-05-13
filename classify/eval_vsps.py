#!/usr/bin/env python

"""Evaluate the VSPS sentiment scores compared to labled training data."""

import extract
import score
import publish

scorer = score.SentimentScorer.from_vaccine_phrases()

# confusion matrix: label, result => count
results = {(x,y) : 0 for x in ['-', 'X'] for y in ['-', 'X']}

for _id, label, text in extract.extract_classified_tweets():
    score = scorer.get_document_score(text, normalize=False)
    if score < 0:
        result = '-'
    else:
        result = 'X'
    results[(label, result)] += 1

print results
