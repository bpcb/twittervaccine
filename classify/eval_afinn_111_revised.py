#!/usr/bin/env python

import score
import evaluate

scorer = score.SentimentScorer.from_afinn_111()
evaluate.evaluate_revised(scorer)
