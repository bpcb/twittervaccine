#!/usr/bin/env python

import extract
import score

scorer = score.SentimentScorer.from_afinn_111()

for _id, text in extract.extract_text(1000):
    s = scorer.get_document_score(text, normalize=False)
    print _id, text, s
