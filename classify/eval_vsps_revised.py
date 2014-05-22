#!/usr/bin/env python

import score
import evaluate

scorer = score.SentimentScorer.from_vaccine_phrases()
evaluate.evaluate_revised(scorer)
