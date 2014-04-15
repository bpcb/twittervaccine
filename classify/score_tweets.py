#!/usr/bin/env python

import extract
import score

scorer = score.SentimentScorer.from_vaccine_phrases()

total = 0
negative = 0
for _id, text in extract.extract_text():
    s = scorer.get_document_score(text, normalize=False)
    total += 1
    if s < 0:
        negative += 1

print '%d of %d negative: %f%%' % (negative, total, float(negative) / total)

